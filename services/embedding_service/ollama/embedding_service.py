
import requests


class EmbeddingService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def embed(self, free_text: str):
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings", json={"model": "nomic-embed-text", "prompt": free_text}
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception:
            return

    # def embed_transactions(self, free_text_list: list[str]):
    #     embeddings = []
    #     for free_text  in free_text_list:
    #         embedding = self.embed_transaction(free_text)
    #         embeddings.append(embedding)
    #     return embeddings
