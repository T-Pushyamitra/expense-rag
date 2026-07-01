from .statement_parser_abstract import StatementParser
from .pdf_statement_parser import PDFStatementParser

class StatementParserFactory:
    @staticmethod
    def get_parser(file_type: str) -> StatementParser:
        parsers = {
            'pdf': PDFStatementParser(),
            # 'xlsx': ExcelParser("Excel Parser"),
            # 'xls': ExcelParser("Excel Parser"),
        }
        parser = parsers.get(file_type.lower(), None)

        
        if not parser:
            return ValueError(f"Unsupported file type {file_type}")
        return parser