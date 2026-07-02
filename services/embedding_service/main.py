from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
import os

from pathlib import Path
import tempfile
import shutil
import uvicorn

from common_lib import setup_logger

load_dotenv()

from pathlib import Path
from .ollama.get_embedding import embed


SERVICE_VERSION = (
    Path(__file__).parent / "VERSION"
).read_text().strip()
    

app = FastAPI(
    title="Embedding Service",
    description="A service for generating embeddings",
    version=SERVICE_VERSION
)


@app.get("/")
def root():
    return {
        "service": "embedding-service",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/embed")
async def embed_text(TransactionText: str):
    embedding = embed(TransactionText)
    return {"embedding": embedding}


def run():
    uvicorn.run(
        "services.embeddings_service.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True
    )