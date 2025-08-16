
from fastapi import FastAPI, Body
from agent import app as graph, chat


app = FastAPI()


@app.get("/")
def root():
    return {"message": "AI Health Navigator API is running"}


@app.post("/navigate")
def navigate(body: dict = Body(...)):
    query = body.get("query")
    if not query:
        return {"error": "Query required"}
    try:
        result = graph.invoke({"query": query})
        return {"response": result["final_response"]}
    except Exception as e:
        return {"error": str(e)}

# Chat endpoint for follow-up questions
@app.post("/chat")
def chat_endpoint(body: dict = Body(...)):
    user_id = body.get("user_id", "default")
    message = body.get("message")
    if not message:
        return {"error": "Message required"}
    try:
        response = chat(user_id, message)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}