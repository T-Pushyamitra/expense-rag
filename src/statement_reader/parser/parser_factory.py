from .parser_abstract import Parser
from .pdf_parser import PDFParser
from .excel_parser import ExcelParser

class ParserFactory:
    @staticmethod
    def get_parser(file_type: str) -> 'Parser':
        parsers = {
            'pdf': PDFParser(),
            'xlsx': ExcelParser("Excel Parser"),
            'xls': ExcelParser("Excel Parser"),
        }
        return parsers.get(file_type.lower(), None)
