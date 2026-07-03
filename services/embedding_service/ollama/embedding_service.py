import requests

class EmbeddingService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _format_transaction_text(self, transaction: dict) -> str:
        transaction_text = (
            f"id:{transaction.get('id')}|"
            f"date:{transaction.get('date')}|"
            f"description:{transaction.get('narration')}|"
            f"{'debited' if transaction.get('transaction_type') == 'DEBIT' else 'credited'} amount:{transaction.get('amount')}|"
            f"balance:{transaction.get('balance')}|"
            f"category:{transaction.get('transaction_category')}"
            )
        return transaction_text

    def embed_transaction(self, transaction: dict):
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": self._format_transaction_text(transaction)
            }
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def embed_transactions(self, transactions: list[dict]):
        embeddings = []
        for transaction in transactions:
            embedding = self.embed_transaction(transaction)
            embeddings.append(embedding)
        return embeddings
    