from .statement_reader_abstract import StatementParser, StatementReader
from .hdfc_statement_reader import HDFCStatementReader
from .axis_statement_reader import AxisStatementReader

class StatementReaderFactory:
    @staticmethod
    def get_reader(bank_name: str) -> StatementReader:
        readers = {
            'hdfc': HDFCStatementReader(),
            'axis': AxisStatementReader()
        }
        return readers.get(bank_name.lower(), None)
