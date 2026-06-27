from abc import ABC, abstractmethod
from typing import Optional, Tuple, Any
import re

class StatementReader(ABC):
    @abstractmethod
    def reader(self, content: str) -> Any:
        """Parse bank statement content and return structured result."""
        pass
    
    @abstractmethod
    def find_date(self, text) -> Optional[Tuple[int, int]]:
        pass
