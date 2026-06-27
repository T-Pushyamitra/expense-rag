In Python, I'd structure it similarly: **Strategy + Factory**, with an optional **Template Method** for shared logic.

## 1. Common Data Model

```python
from dataclasses import dataclass
from datetime import date


@dataclass
class Transaction:
    transaction_date: date
    description: str
    amount: float
    balance: float


@dataclass
class BankStatement:
    transactions: list[Transaction]
```

---

## 2. Strategy Pattern

Define a common parser interface.

```python
from abc import ABC, abstractmethod


class StatementParser(ABC):

    @abstractmethod
    def parse(self, file_path: str) -> BankStatement:
        pass
```

---

## 3. Template Method (Shared Workflow)

Most banks follow the same flow:

```python
class BaseStatementParser(StatementParser):

    def parse(self, file_path: str) -> BankStatement:
        raw_data = self.read_file(file_path)
        transactions = self.parse_transactions(raw_data)
        return BankStatement(transactions)

    @abstractmethod
    def read_file(self, file_path: str):
        pass

    @abstractmethod
    def parse_transactions(self, raw_data):
        pass
```

---

## 4. Bank-Specific Strategies

### HDFC Parser

```python
class HDFCParser(BaseStatementParser):

    def read_file(self, file_path):
        with open(file_path, "r") as f:
            return f.readlines()

    def parse_transactions(self, lines):
        transactions = []

        for line in lines:
            # HDFC-specific parsing
            parts = line.strip().split(",")

            transactions.append(
                Transaction(
                    transaction_date=parts[0],
                    description=parts[1],
                    amount=float(parts[2]),
                    balance=float(parts[3]),
                )
            )

        return transactions
```

### ICICI Parser

```python
class ICICIParser(BaseStatementParser):

    def read_file(self, file_path):
        with open(file_path, "r") as f:
            return f.readlines()

    def parse_transactions(self, lines):
        transactions = []

        for line in lines:
            # ICICI-specific parsing logic
            pass

        return transactions
```

---

## 5. Factory Pattern

```python
class ParserFactory:

    _parsers = {
        "HDFC": HDFCParser,
        "ICICI": ICICIParser,
    }

    @classmethod
    def get_parser(cls, bank_name: str) -> StatementParser:
        parser_class = cls._parsers.get(bank_name)

        if not parser_class:
            raise ValueError(
                f"No parser found for bank: {bank_name}"
            )

        return parser_class()
```

Usage:

```python
parser = ParserFactory.get_parser("HDFC")

statement = parser.parse("statement.csv")

print(statement.transactions)
```

---

## 6. Better for Many Banks (Recommended)

If you're parsing 20–100 banks, don't create 100 parser classes.

Instead create:

```python
class GenericCsvParser:
    def __init__(self, config):
        self.config = config

    def parse(self, file_path):
        ...
```

Configuration:

```python
BANK_CONFIGS = {
    "HDFC": {
        "date_col": 0,
        "desc_col": 1,
        "amount_col": 2,
        "balance_col": 3,
        "date_format": "%d/%m/%Y",
    },
    "ICICI": {
        "date_col": 2,
        "desc_col": 4,
        "amount_col": 5,
        "balance_col": 6,
        "date_format": "%Y-%m-%d",
    },
}
```

Then:

```python
parser = GenericCsvParser(BANK_CONFIGS["HDFC"])
```

This is much easier to maintain when formats differ mostly in:

* Column positions
* Date formats
* Header names
* Debit/Credit column names

### Architecture I'd recommend

```text
StatementDetector
        ↓
ParserFactory
        ↓
GenericParser
        ↓
BankConfig
        ↓
Normalized Transaction Model
```

Only create a custom strategy class when a bank's statement structure is fundamentally different (e.g., PDF table extraction vs CSV vs Excel). For normal variations in columns and formats, use configuration rather than new parser classes.
