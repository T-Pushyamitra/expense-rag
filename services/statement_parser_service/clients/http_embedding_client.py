from .embedding_client import EmbeddingClient
from common_lib import Transaction
from httpx import Client
import json

# TODO: Add retry logic and error handling for the HTTP requests
# TODO: Add logging for the requests and responses
# TODO: Add support for async requests if needed
# TODO: Use Context Managers for the HTTP client to ensure proper resource cleanup
class HttpEmbeddingClient(EmbeddingClient):

    def __init__(self, base_url: str):
        self.client = Client(base_url=base_url)

    def embed_transaction(self, transaction: Transaction):
        response = self.client.post(
            "/transactions/embed",
            json={'transactions': json.dumps(transaction.to_dict(), default=str)}
        )
        response.raise_for_status()
        
    def embed_transactions(self, transactions: list[Transaction]):
        response = self.client.post(
            "/transactions/embed/batch",
            json={'transactions': [json.dumps(t.to_dict(), default=str) for t in transactions]}
        )

        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close() 