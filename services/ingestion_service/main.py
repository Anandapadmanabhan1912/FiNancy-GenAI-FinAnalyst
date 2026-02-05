from fastapi import FastAPI
from pydantic import BaseModel
from ingest import ingest_urls

app = FastAPI(title="Ingestion Service")

class IngestRequest(BaseModel):
    urls: list[str]

@app.post("/ingest")
def ingest(req: IngestRequest):
    return ingest_urls(req.urls)
