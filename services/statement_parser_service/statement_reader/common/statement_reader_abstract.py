from abc import ABC, abstractmethod


class StatementReader(ABC):
    @abstractmethod
    def reader(self):
        """Parse bank statement content and return structured result."""
        pass
