import logging
import re
from datetime import datetime

from src.utils.transactions import Transaction

from .parser.parser_factory import ParserFactory
from .statement_reader_abstract import StatementReader
from typing import Optional, List, Tuple
from src.utils.constants import DEBIT, CREDIT

BAD_ROW_KEYWORDS = {'transaction', 'closing'}

logger = logging.getLogger("exepnse-rag")

class AxisStatementReader(StatementReader):
    
    datetime_format: str = "%d-%m-%Y"
    DATE_REGEX: str = r"(?<!\d)\d{2}-\d{2}-\d{4}(?!\d)"
    
    
    def __init__(self, file_path: str, password: str = None):
        super().__init__()
        self.file_path: str = file_path
        self.__password: str = password
        self.transactions: List[Transaction] = []
        self._parser: ParserFactory = ParserFactory.get_parser(file_path.split('.')[-1])
        self.opening_blanance = 0.0
    
    def reader(self) -> List[Transaction]:
        if self._parser is None:
            raise ValueError(f"Unsupported file type for {self.file_path}")

        rows = self._parser.parse(self.file_path, self.__password)
                
        self._parse_transaction_rows(rows)
        self.convert_transaction()
        return self.transactions
    
    def find_date(self, text) -> Optional[Tuple[int, int]]:
        match = re.search(self.DATE_REGEX, text)
        if match:
            return match.group()
        return None

    def convert_transaction(self) -> None:
        current_balance = self.opening_blanance
        
        for transaction in self.transactions:
            try:
                cols = transaction.non_empty_columns()[:-1]
                date = None

                date = self.find_date(str(cols[0])) or self.find_date(str(cols[1]))

                if not date:
                    raise Exception("No date found for transaction")

                transaction.date = datetime.strptime(date, self.datetime_format)
                transaction.amount = self.float_amount(cols[-2])
                transaction.balance = self.float_amount(cols[-1])
                
                transaction.narration = "".join(cols[1:-2])
                transaction.narration = transaction.narration.replace(date, "")
                
                is_debit = transaction.balance < current_balance
                transaction.transaction_type = DEBIT if is_debit else CREDIT
                
                current_balance = transaction.balance
                
                if not(bool(transaction.date) and bool(transaction.amount) and bool(transaction.balance) and bool(transaction.narration)):
                    raise Exception(f"Transaction failed {transaction.columns}")
                logger.debug(transaction)
            except ValueError as e:
                print(e)

    @staticmethod
    def _is_bad_row(row: Transaction) -> bool:
        return any(k in row.text.lower() for k in BAD_ROW_KEYWORDS)
    
    @staticmethod
    def float_amount(amount) -> float:
        return float(amount.replace(",", ""))
    
    def _parse_transaction_rows(self, rows):
        current_transaction: Transaction = None
        
        found_bad_row = False        
        
        for idx, _row in enumerate(rows):
            row = Transaction(_row)
            
            if row.is_empty:
                continue
            
            if row.text.lower() in "opening":
               for col in row.non_empty_columns():
                    if col.isalnum():
                        self.opening_blanance = self.float_amount(col)
                  
            # If transaction row is found add transaction to list
            if row.is_transaction(self.find_date):
                found_bad_row = False
                if current_transaction:
                    self.transactions.append(current_transaction)
                current_transaction = row  
            
            if found_bad_row or self._is_bad_row(row):
                found_bad_row = True
                row.mark_as_bad_row
                
            if (current_transaction and current_transaction is not row) and not found_bad_row:
                current_transaction.add_child(row)
                    
        # Last transaction
        self.transactions.append(current_transaction)
