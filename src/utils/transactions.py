import re
from typing import Optional, Sequence, List
from datetime import datetime

class Transaction:


    def __init__(self, row: Sequence[Optional[str]]):
        self.columns = list(row)
        self.linked_rows: list = []
        self.is_bad_row: bool = False
        self.amount: float = None
        self.balance: float = None
        self.date: datetime = None
        self.narration: str = None
        self.transaction_type: str = None

    @property
    def text(self) -> str:
        return "".join(
            str(x).strip()
            for x in self.columns
            if x
        )

    @property
    def is_empty(self) -> bool:
        return not self.text

    @property
    def is_header(self) -> bool:
        value = self.text.lower()
        return "date" in value and "narration" in value
    
    @property
    def mark_as_bad_row(self) -> bool:
        self.is_bad_row
        return self
    
    def is_transaction(self, find_date: callable) -> bool:
        for col in self.columns:
            if col and find_date(str(col)):
                return True
        return False
    
    def non_empty_columns(self) -> List[str]:
        return [
            col for col in self.columns
            if col
        ]

    def add_child(self, row) -> None:
        if row.is_empty:
            return
        self.linked_rows.append(row)
        
    def __repr__(self):
        return (
            f"<Transaction "
            f"{self.date=} "
            f"{self.amount=} "
            f"{self.balance=} "
            f"{self.transaction_type=} "
            f"children={len(self.linked_rows)}>"
        )
    