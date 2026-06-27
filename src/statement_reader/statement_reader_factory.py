from .statement_reader_abstract import StatementParser, StatementReader
from .hdfc_statement_reader import HDFCStatementParser

class StatementReaderFactory:
    @staticmethod
    def get_reader(bank_name: str) -> StatementReader:
        readers = {
            'hdfc': HDFCStatementParser(),
            # Add more banks and their corresponding readers here
        }
        return readers.get(bank_name.lower(), None)
