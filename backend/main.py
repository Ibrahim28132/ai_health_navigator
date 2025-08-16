from fastapi import FastAPI, Body
from agent import app as graph

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