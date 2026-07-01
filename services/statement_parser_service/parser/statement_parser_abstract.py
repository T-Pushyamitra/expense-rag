from abc import ABC, abstractmethod
from typing import Iterator


class StatementParser(ABC):

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def parse(self, file_path: str, password: str=None) -> Iterator[list]:
        pass