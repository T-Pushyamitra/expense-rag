from ..common.statement_exceptions import UnsupportedFileException
from .pdf_statement_parser import PDFStatementParser
from .statement_parser_abstract import StatementParser


class StatementParserFactory:
    @staticmethod
    def get_parser(file_type: str) -> StatementParser:
        parsers = {
            'pdf': PDFStatementParser()
        }
        parser = parsers.get(file_type.lower(), None)

        
        if not parser:
            return UnsupportedFileException(f"Unsupported file type {file_type}")
        return parser