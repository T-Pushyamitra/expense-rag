from fastapi import Depends, FastAPI, status
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from pathlib import Path
from sqlalchemy.orm import Session
import uvicorn


from pathlib import Path

from .ollama import EmbeddingService
from .settings import SETTINGS
from pydantic import BaseModel
from .database.sessions.metadata_session import get_metadata_session, init_db as metadata_init_db

from .service.transaction_service import TransactionService
from .service.query_service import QueryService
from common_lib.enum.route_enum import RouteEnum

import json
from dataclasses import asdict
import logging

logger = logging.getLogger("embedding-service")

SERVICE_VERSION = (Path(__file__).parent / "VERSION").read_text().strip()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Initialize the database
#     from services.embedding_service.database.sessions.metadata_session import init_db
#     init_db()
#     yield


app = FastAPI(
    title=SETTINGS.app_name,
    description=SETTINGS.app_description,
    version=SERVICE_VERSION,
    # lifespan=lifespan
)


@app.on_event("startup")
def startup():
    metadata_init_db()


@app.get("/")
def root():
    return {"service": SETTINGS.app_name, "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


#### API RESPONSE
class ErrorModel(BaseModel):
    message: str


class EmbeddingResponse(BaseModel):
    status: int
    error: ErrorModel | None = None


class BatchEmbedRequest(BaseModel):
    transactions: list


class Filters(BaseModel):
    amount_gt: int
    amount_lt: int
    categories: list[str]
    months: list[str]
    semantic_query: list[str]


class QueryRequest(BaseModel):
    free_text: str
    filters: Filters | None = None
    model_name: str | None = None
    route: RouteEnum


class QueryResponse(BaseModel):
    result: str | list
    error: ErrorModel | None = None


@app.post("/transactions/embed/batch")
def embed_transactions(request: BatchEmbedRequest, metadata_session: Session = Depends(get_metadata_session)):

    try:
        transactions = request.transactions

        if not transactions:
            return EmbeddingResponse(status=status.HTTP_200_OK)
        transaction_service = TransactionService(metadata_session)
        transaction_service.save_transactions(transactions=transactions)
        return EmbeddingResponse(status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Failed to parse {e}")
        return EmbeddingResponse(
            status=status.HTTP_400_BAD_REQUEST, error=ErrorModel(message="Failed to parse the embedding")
        )


@app.post("/query/embed")
def embed_query(request: QueryRequest, metadata_session: Session = Depends(get_metadata_session)):

    try:
        service = QueryService(metadata_session)
        results = service.search(request.free_text)
        return QueryResponse(result=results)
    except Exception as e:
        logger.error(f"Failed to parse {e}")
        return EmbeddingResponse(
            status=status.HTTP_400_BAD_REQUEST, error=ErrorModel(message="Failed to parse the embedding")
        )


@app.get("/model/version")
def ollama_version():

    try:
        service = QueryService()
        version = service.get_version()
        return QueryResponse(result=str(version))
    except Exception as e:
        logger.error(f"Failed to parse {e}")
        return EmbeddingResponse(status=status.HTTP_400_BAD_REQUEST, error=ErrorModel(message="Failed while embedding"))


@app.get("/model/ps")
def ollama_models():
    try:
        service = QueryService()
        models = service.get_models()
        return QueryResponse(result=str(models))
    except Exception as e:
        logger.error(f"Failed to parse {e}")
        return EmbeddingResponse(status=status.HTTP_400_BAD_REQUEST, error=ErrorModel(message="Failed while embedding"))


def run():
    uvicorn.run(
        "services.embedding_service.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", SETTINGS.app_port)),
        reload=True,
        reload_dirs=["services/embedding_service", "common_lib"],
    )
