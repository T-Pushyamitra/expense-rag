from typing import Any

from ..common.row_utils import clean_rows, is_bad_row, is_row_empty, is_transaction_row, normalize_row
from ..common.transaction_utils import Transaction, custom_float, find_date, get_transaction_type
from .rules import BAD_ROW_KEYWORDS, DATE_REGEX, OPENING_BALANCE


class AXISStatementExtractor:
    """
    This class is responsible for extracting the statement of AXIS Bank.
    """

    def __init__(self, file_name):
        self.opening_balance = 0.0
        self.file_name = file_name

    def feeder(self, pages: list[list[str]]) -> list[Transaction]:
        """
            Feed tables read from parser and convert to transaction

        Args:
            pages (list[list[str]]): Pass the pages found from the statement file

        Returns:
            list[Transaction]:
        """
        transactions = []
        self._get_opening_balance(pages[0])

        for idx, page in enumerate(pages):
            page_transactions = self._parse_transaction_rows(page, idx + 1)
            transactions.extend(page_transactions)

        return transactions

    def _get_opening_balance(self, page: list[list[str]]) -> float:
        """
        This is used to get the opening balance from the statement

        Args:
            page (list[list[str]]): Expected last page

        Returns:
            float:
        """

        for row in page:
            normalized_row = normalize_row(row).lower()

            if OPENING_BALANCE in normalized_row:
                rows = clean_rows(row)
                self.opening_balance = custom_float(rows[-1])
                break

        return None

    def _build_transaction(self, transaction: dict, page_number: int, transaction_number: int) -> Transaction:
        """
            Convert the cleaned transaction to Transaction dataclass

        Args:
            transaction (dict): pass the transaction dict
            page_number (int): Number of Page from statement file
            transaction_number (int): transaction number from the statement file

        Returns:
            Transaction
        """
        try:
            main_row = clean_rows(transaction["main_row"])[:-1]
            child_rows = [clean_rows(row) for row in transaction["child_rows"]]
            transaction_date = find_date(main_row[0], DATE_REGEX)
            transaction_amount = custom_float(main_row[-2])
            transaction_balance = custom_float(main_row[-1])
            transaction_type = get_transaction_type(transaction_balance, self.opening_balance)

            transaction_desc = normalize_row(main_row, remove_digits=True)
            transaction_desc += "".join([normalize_row(row, remove_digits=True) for row in child_rows])
            transaction_desc.replace(transaction_date, "")

            ## Update the opening_balance
            self.opening_balance = transaction_balance

            return Transaction(
                date=transaction_date,
                amount=transaction_amount,
                balance=transaction_balance,
                type=transaction_type,
                description=transaction_desc,
                file_name=self.file_name,
                page_no=page_number,
                transaction_no=transaction_number,
            )
        except Exception as e:
            print(f"Error building transaction: {e}")
            print(f"Failed building transaction on page {page_number}")
            return None

    def _parse_transaction_rows(self, rows: list[list[str]], page_no: int) -> list[Any] | None:
        """
        Clean and gather the transactions from the statement files

        Args:
            rows (list[list[str]]):
            page_no (int):

        Returns:
            list[Any] | None:
        """
        found_bad_row = False
        previous_row = None

        current_transaction = {"main_row": [], "child_rows": []}
        transactions = []
        transaction_number = 1

        try:
            for row in rows:
                # Skip empty rows
                if is_row_empty(row):
                    continue

                # If transaction is found
                if is_transaction_row(row, DATE_REGEX):
                    found_bad_row = False

                    if current_transaction["main_row"]:
                        txn = self._build_transaction(
                            current_transaction, page_number=page_no, transaction_number=transaction_number
                        )
                        transaction_number += 1
                        if txn:
                            transactions.append(txn)

                    current_transaction = {"main_row": [], "child_rows": []}
                    current_transaction["main_row"] = row

                # Check if the row is a bad row
                if found_bad_row or is_bad_row(row, BAD_ROW_KEYWORDS):
                    found_bad_row = True

                    if current_transaction and previous_row and any("From :" in cell for cell in previous_row):
                        found_bad_row = False

                if current_transaction["main_row"] and current_transaction["main_row"] != row and not found_bad_row:
                    current_transaction["child_rows"].append(row)

                previous_row = row

            # Add the last transaction
            if current_transaction["main_row"]:
                txn = self._build_transaction(
                    current_transaction, page_number=page_no, transaction_number=transaction_number
                )
                transaction_number += 1
                if txn:
                    transactions.append(txn)

            return transactions
        except Exception as e:
            print(f"Error while parsing rows: {e}")
            print(f"Current row: {row}")
