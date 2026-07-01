from .statement_reader_abstract import StatementReader
from .hdfc_statement_reader import HDFCStatementReader
from .axis_statement_reader import AxisStatementReader

class StatementReaderFactory:
    @staticmethod
    def get_reader(bank_name: str, file_path: str, password: str = None) -> StatementReader:
        readers = {
            'hdfc': HDFCStatementReader,
            'axis': AxisStatementReader
        }
        reader_class = readers.get(bank_name.lower(), None)

        if not reader_class:
            raise ValueError("Unsupported bank: {bank_name}")
        return reader_class(file_path, password)