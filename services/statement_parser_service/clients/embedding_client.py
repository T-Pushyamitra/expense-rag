from abc import ABC, abstractmethod


class EmbeddingClient(ABC):
    @abstractmethod
    def embed_transaction(self, transaction):
        pass
