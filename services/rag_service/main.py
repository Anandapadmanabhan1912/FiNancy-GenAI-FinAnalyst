from fastapi import FastAPI
from pydantic import BaseModel
from rag import answer_query

app = FastAPI(title="RAG Service")

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query(req: QueryRequest):
    return answer_query(req.question)
