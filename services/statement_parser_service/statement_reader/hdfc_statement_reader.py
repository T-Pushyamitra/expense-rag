import logging
import re
import uuid
from datetime import datetime
from typing import Optional, List

from common_lib import Transaction

# from ..category import categorize
from ..parser import StatementParserFactory, StatementParser
from ..statement_reader.statement_reader_abstract import StatementReader

from ..utils.constants import DEBIT, CREDIT


logger = logging.getLogger("exepnse-rag")

class HDFCStatementReader(StatementReader):
    
    DATETIME_FORMAT: str = "%d/%m/%y"
    DATE_REGEX: str = r"(?<!\d)\d{2}/\d{2}/\d{2}(?!\d)"
    BAD_ROW_KEYWORDS = {'closingbalance', 'account', 'opening'}
    
    
    def __init__(self, file_path: str, password: str = None):
        super().__init__()
        self.file_path: str = file_path
        self._password: str = password
        self._parser: StatementParser = StatementParserFactory.get_parser(file_path.split('.')[-1])
    
    def find_date(self, text) -> Optional[str]:
        match = re.search(self.DATE_REGEX, text)
        if match:
            return match.group()
        return None
    
    def reader(self) -> List[Transaction]:
        document_id = self.file_path.capitalize().split('/')[-1] + str(uuid.uuid4())

        metadata = {"document_id": document_id, "file_name": self.file_path.split('/')[-1], "pages": {}}
        page_number = 1
        if self._parser is None:
            raise ValueError(f"Unsupported file type for {self.file_path}")

        table = self._parser.parse(self.file_path, self._password)
        
        for rows in table:
            transactions = self._parse_transaction_rows(rows)
            metadata["pages"][f"1-{page_number}"] = len(transactions)
            page_number += 1
            
        return metadata
    
    def get_opening_balance(self) -> Optional[float]:
        OPENING_BALANCE = "opening"
        table = self._parser.get_last_page(self.file_path, self._password)
        
        idx = [idx for idx, row in enumerate(table) if row and OPENING_BALANCE in self.normalize_row(row)][0]
        for col in table[idx+1]:
            if col:
                return self.float_amount(col)
        return None

    def _convert_transaction(self, transactions) -> Optional[Transaction]:
        current_balance = self.get_opening_balance()
        
        for transaction in transactions:
            try:
                cols = transaction.non_empty_columns()
                date = None

                date = self.find_date(str(cols[0])) or self.find_date(str(cols[1]))

                if not date:
                    raise Exception("No date found for transaction")

                transaction.date = datetime.strptime(date, self.DATETIME_FORMAT)
                transaction.amount = self.float_amount(cols[-2])
                transaction.balance = self.float_amount(cols[-1])
                transaction.narration = "".join(transaction.columns[:-2])

                for row in transaction.linked_rows:
                    if row.is_bad_row:
                        continue
                    transaction.narration += "".join(row.columns)

                transaction.narration = transaction.narration.replace(date, "")
                is_debit = transaction.balance < current_balance
                transaction.transaction_type = DEBIT if is_debit else CREDIT
                current_balance = transaction.balance
                
                if not(bool(transaction.date) and bool(transaction.amount) and bool(transaction.balance) and bool(transaction.narration)):
                    raise Exception(f"Transaction failed {transaction.columns}")
                
                return transaction
                # transaction.transaction_category = categorize(transaction.narration)                
            except ValueError as e:
                print(e)

    def _parse_transaction_rows(self, rows) -> List[Transaction]:
        current_transaction: Transaction = None
        found_bad_row = False        
        previous_row: Transaction = None
        
        transactions = []
        for _row in rows:
            row = Transaction(_row)
            
            if row.is_empty:
                continue

            # If transaction row is found add transaction to list
            if row.is_transaction(self.find_date):
                found_bad_row = False
                if current_transaction:
                    transactions.append(self._convert_transaction([current_transaction]))
                current_transaction = row  
            
            if found_bad_row or self._is_bad_row(row, self.BAD_ROW_KEYWORDS):
                found_bad_row = True
                row.mark_as_bad_row
                if current_transaction and "From :" in previous_row.text:
                    found_bad_row = False
                
            if (current_transaction and current_transaction is not row) and not found_bad_row:
                current_transaction.add_child(row)
            
            previous_row = row
        
        # Last transaction
        transactions.append(self._convert_transaction([current_transaction]))
        
        return transactions