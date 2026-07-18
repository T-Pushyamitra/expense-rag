import json
from dataclasses import asdict

from httpx import Client

from ..statement_reader.common.transaction_utils import Transaction
from .embedding_client import EmbeddingClient


# TODO: Add retry logic and error handling for the HTTP requests
# TODO: Add logging for the requests and responses
# TODO: Add support for async requests if needed
# TODO: Use Context Managers for the HTTP client to ensure proper resource cleanup
class HttpEmbeddingClient(EmbeddingClient):
    def __init__(self, base_url: str = None):
        self.client = Client(base_url=base_url)

    def embed_transaction(self, transaction: Transaction):
        response = self.client.post(
            "/transactions/embed", json={"transactions": json.dumps(asdict(transaction), default=str)}
        )
        response.raise_for_status()

    def embed_transactions(self, transactions: list[Transaction]):
        response = self.client.post(
            "/transactions/embed/batch",
            json={"transactions": [json.dumps(asdict(t), default=str) for t in transactions]},
        )

        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()
