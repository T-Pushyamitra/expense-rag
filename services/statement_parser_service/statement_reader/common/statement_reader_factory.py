from ..axis.axis_statement_reader import AXISStatementReader
from ..common.statement_exceptions import UnsupportedFileException
from ..hdfc.hdfc_statement_reader import HDFCStatementReader
from .statement_reader_abstract import StatementReader


class StatementReaderFactory:
    @staticmethod
    def get_reader(bank_name: str, file_path: str, password: str = None) -> StatementReader:
        readers = {
            'hdfc': HDFCStatementReader,
            'axis': AXISStatementReader   
        }
        reader_class = readers.get(bank_name.lower(), None)

        if not reader_class:
            raise UnsupportedFileException(f"Unsupported bank: {bank_name}")
        return reader_class(file_path, password)