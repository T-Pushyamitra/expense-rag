import requests


def embed(transaction_text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": transaction_text
        }
    )

    embedding = response.json()["embedding"]
    return embedding