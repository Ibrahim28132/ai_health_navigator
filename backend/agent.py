import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel
from dotenv import load_dotenv
import googlemaps
import requests
from tavily import TavilyClient

load_dotenv(dotenv_path="../.env")

# Clients
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
openweather_key = os.getenv("OPENWEATHER_API_KEY")


# State with context
class State(TypedDict):
    query: str
    symptoms: str
    location: str
    actions: List[str]
    triage: str
    hospitals: List[dict]
    advisories: str
    weather: str
    final_response: str
    context: List[dict]  # Conversation history

# Models
class Extract(BaseModel):
    symptoms: str
    location: str

class Plan(BaseModel):
    actions: List[str]
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "actions": ["medical", "hospitals", "advisories", "weather"]
                }
            ]
        }

# Extract node
def node_extract(state: State) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("Extract symptoms and location. No location? Use 'Unknown'."),
        HumanMessagePromptTemplate.from_template("{query}")
    ])
    structured_llm = llm.with_structured_output(Extract)
    response = structured_llm.invoke(prompt.format_messages(query=state["query"]))
    return {"symptoms": response.symptoms, "location": response.location}

# Planner node
def node_planner(state: State) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "Plan actions for symptoms '{symptoms}' in '{location}'. Return ONLY these action keywords: "
            "medical (always if symptoms), hospitals (if location known), advisories, weather (if location known). "
            "Do not add descriptions or explanations, just the keywords."
        ),
    ])
    structured_llm = llm.with_structured_output(Plan)
    response = structured_llm.invoke(prompt.format_messages(symptoms=state["symptoms"], location=state["location"]))
    return {"actions": response.actions}

# Helpers
def get_medical_triage(symptoms: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "Provide general info for '{symptoms}'. Suggest causes, urgency, advice. No diagnosis. Consult doctor."
        ),
    ])
    return llm.invoke(prompt.format_messages(symptoms=symptoms)).content

def get_hospitals(location: str) -> List[dict]:
    try:
        geocode = gmaps.geocode(location)
        if not geocode:
            return []
        lat_lng = geocode[0]['geometry']['location']
        places = gmaps.places_nearby(location=lat_lng, radius=10000, type='hospital')
        return [{"name": p["name"], "address": p.get("vicinity", "N/A"), "rating": p.get("rating", "N/A")} for p in places.get("results", [])]
    except Exception as e:
        return [{"error": str(e)}]

def get_advisories(location: str) -> str:
    try:
        results = tavily.search(f"public health advisories in {location}", max_results=3)
        return "\n\n".join([r["content"] for r in results.get("results", [])]) or "No advisories."
    except Exception as e:
        return f"Error: {str(e)}"

def get_weather(location: str) -> str:
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={openweather_key}&units=metric"
        data = requests.get(url).json()
        if data.get("cod") != 200:
            return "Unavailable."
        return f"{data['weather'][0]['description']}, {data['main']['temp']}°C. Consider health impact."
    except Exception as e:
        return f"Error: {str(e)}"

# Execute node
def node_execute(state: State) -> dict:
    actions = state["actions"]
    updates = {}
    if "medical" in actions:
        updates["triage"] = get_medical_triage(state["symptoms"])
    if "hospitals" in actions and state["location"] != "Unknown":
        updates["hospitals"] = get_hospitals(state["location"])
    if "advisories" in actions:
        updates["advisories"] = get_advisories(state["location"])
    if "weather" in actions and state["location"] != "Unknown":
        updates["weather"] = get_weather(state["location"])
    return updates

# Critic node
def node_critic(state: State) -> dict:
    hospitals_str = "\n".join([f"- {h['name']}, {h['address']} (Rating: {h['rating']})" for h in state.get("hospitals", [])]) or "None."
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "Compile: Triage: {triage}\nAdvisories: {advisories}\nWeather: {weather}\nHospitals:\n{hospitals_str}\n"
            "Structure response. Add disclaimer: 'Not medical advice. Consult professional. Emergencies: seek help.'"
        ),
    ])
    response = llm.invoke(prompt.format_messages(
        triage=state.get("triage", "None"), advisories=state.get("advisories", "None"),
        weather=state.get("weather", "None"), hospitals_str=hospitals_str
    ))
    return {"final_response": response.content}


# Graph
graph = StateGraph(State)
graph.add_node("extract", node_extract)
graph.add_node("planner", node_planner)
graph.add_node("execute", node_execute)
graph.add_node("critic", node_critic)
graph.set_entry_point("extract")
graph.add_edge("extract", "planner")
graph.add_edge("planner", "execute")
graph.add_edge("execute", "critic")
graph.add_edge("critic", END)
app = graph.compile()

# Context manager for chat
from collections import defaultdict
user_contexts = defaultdict(list)  # user_id -> list of messages

def chat(user_id: str, message: str) -> str:
    # Append user message to context
    user_contexts[user_id].append({"role": "user", "content": message})
    # Build context for LLM
    context = user_contexts[user_id][-5:]  # last 5 messages
    # Use LLM to respond
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a helpful health assistant. Use context to answer follow-up questions. If medical, remind user to consult a professional."),
        *[HumanMessagePromptTemplate.from_template(m["content"]) for m in context if m["role"] == "user"]
    ])
    response = llm.invoke(prompt.format_messages())
    user_contexts[user_id].append({"role": "assistant", "content": response.content})
    return response.content