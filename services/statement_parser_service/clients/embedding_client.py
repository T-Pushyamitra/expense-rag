from abc import ABC, abstractmethod

from common_lib import Transaction


class EmbeddingClient(ABC):

    @abstractmethod
    def embed_transaction(self, transaction: Transaction):
        pass