from fastapi import FastAPI
from dotenv import load_dotenv
import os

from pathlib import Path
import uvicorn


from pathlib import Path

from services.embedding_service.settings import settings
from .ollama import EmbeddingService
from common_lib import Transaction
from typing import List
from .settings import SETTINGS
from pydantic import BaseModel

SERVICE_VERSION = (
    Path(__file__).parent / "VERSION"
).read_text().strip()
    

app = FastAPI(
    title=SETTINGS.app_name,
    description=SETTINGS.app_description,
    version=SERVICE_VERSION
)

embedding_service = EmbeddingService(base_url=SETTINGS.ollama_api_embedding_service_url)

@app.get("/")
def root():
    return {
        "service": SETTINGS.app_name,
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

class BatchEmbedRequest(BaseModel):
    transactions: list

@app.post("/transactions/embed/batch")
async def embed_text(request: BatchEmbedRequest):
    for tx in request.transactions:
        embedding_service.embed_transaction(tx)
    return "Embeddings generated for all transactions", None


def run():
    uvicorn.run(
        "services.embedding_service.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", SETTINGS.app_port)),
        reload=True,
        reload_dirs=["services/embedding_service", "common_lib"]
    )