from fastapi import FastAPI
from pydantic import BaseModel
from search import search_news

app = FastAPI(title="Search Service")

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
def search(req: SearchRequest):
    return {"urls": search_news(req.query)}
