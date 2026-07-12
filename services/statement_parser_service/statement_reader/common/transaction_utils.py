import re
from dataclasses import dataclass


@dataclass
class Transaction:
    date: str
    amount: float
    balance: float
    description: str
    type: str
    file_name: str 
    page_no: int
    transaction_no: int
    
    
def find_date(text, regex) -> str | None:
    match = re.search(regex, text)
    if match:
        return match.group()
    return None

def custom_float(amount: str) -> float:
    try:
        return float(amount)
    except ValueError:
        return float(amount.replace(",", ""))
  
@staticmethod
def get_transaction_type(current: float, previous: float) -> bool:
    return "DEBIT" if current < previous else "CREDIT"