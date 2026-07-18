from sqlalchemy.orm import Session
from sqlmodel import select

from ..database.models.transaction import Transaction, TransactionCreate
from ..settings import SETTINGS
from ..ollama import EmbeddingService
from ..database.models.transaction_embedding import TransactionEmbedding

import json
import requests


class QueryService:
    def __init__(self, session: Session = None):
        self.embedding_service = EmbeddingService(base_url=SETTINGS.ollama_api_embedding_service_url)
        self.base_url = SETTINGS.ollama_api_embedding_service_url
        self.session: Session = session

    def search(self, query: str, filters: dict = {}, route: str = None, top_k: int = 5):
        # 1. Embed query
        query_embedding = self.embedding_service.embed(query)
        print(query, query_embedding)

        # 2. Build vector DB filter
        where = filters

        if route:
            where["route"] = route

        # 3. Search vector store
        statement = (
            select(Transaction)
            .join(
                TransactionEmbedding,
                Transaction.id == TransactionEmbedding.transaction_id,
            )
            .order_by(TransactionEmbedding.embedding.cosine_distance(query_embedding))
            .limit(top_k)
        )

        results = self.session.exec(statement).all()
        return results

    def get_version(self):
        try:
            response = requests.get(f"{self.base_url}/api/version")
            response.raise_for_status()
            version = response.json()
            return version
        except Exception as e:
            return e

    def get_models(self):
        try:
            response = requests.get(f"{self.base_url}/api/ps")
            response.raise_for_status()
            version = response.json()
            return version
        except Exception as e:
            return e
