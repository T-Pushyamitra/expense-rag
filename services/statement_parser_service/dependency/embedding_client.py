from collections.abc import Generator

from services.statement_parser_service.clients.http_embedding_client import HttpEmbeddingClient
from services.statement_parser_service.settings import SETTINGS


def get_embedding_client() -> Generator[HttpEmbeddingClient, None, None]:
    client = HttpEmbeddingClient(base_url=SETTINGS.embedding_service_url)
    try:
        yield client
    finally:
        client.close()
