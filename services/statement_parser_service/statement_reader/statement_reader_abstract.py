from abc import ABC, abstractmethod
from typing import Optional, Tuple, Any
import re

from ..transaction import Transaction

class StatementReader(ABC):
    @abstractmethod
    def reader(self, content: str) -> Any:
        """Parse bank statement content and return structured result."""
        pass
    
    @abstractmethod
    def find_date(self, text) -> Optional[Tuple[int, int]]:
        pass

    # Fix: Add type Transaction
    @staticmethod
    def _is_bad_row(row: Transaction, BAD_ROW_KEYWORDS) -> bool:
        return any(k in row.text.lower() for k in BAD_ROW_KEYWORDS)
    
    @staticmethod
    def float_amount(amount) -> float:
        try:
            return float(amount)
        except ValueError as e:
            return float(amount.replace(",", ""))
        except AttributeError as e:
            raise ValueError("Expected float or string values")

    @staticmethod
    def normalize_row(row: list) -> str:
        return "".join(row).lower()
    