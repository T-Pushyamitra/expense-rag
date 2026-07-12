import logging

import pdfplumber
from pdfminer.pdfdocument import PDFPasswordIncorrect
from pdfminer.pdfparser import PDFSyntaxError

from ..common.statement_exceptions import CorruptedPdfException, InvalidPasswordException, StatementReaderException
from .statement_parser_abstract import StatementParser

logger = logging.getLogger("exepnse-rag")

class PDFStatementParser(StatementParser):
    def __init__(self) -> None:
        super().__init__("PDF Parser")

    @staticmethod
    def _get_table_settings(settings):
        return {
              "vertical_strategy": settings.get("vertical_strategy", "text"),
               "horizontal_strategy": settings.get("horizontal_strategy", "text"),
               "min_words_vertical": settings.get("min_words_vertical", 2),
               "min_words_horizontal": settings.get("min_words_horizontal", 1),
               "snap_tolerance": settings.get("snap_tolerance", 5),
               "join_tolerance": settings.get("join_tolerance", 5),
               "intersection_tolerance": settings.get("intersection_tolerance", 5),
               "text_x_tolerance": settings.get("text_x_tolerance", 2),
               "text_y_tolerance": settings.get("text_y_tolerance", 3),
            }
        
    def parse(self, file_path: str, password: str, **table_settings_args) -> list[list[list[str]]]:
        try:
            
            table_settings = self._get_table_settings(table_settings_args)

            pages = []

            with pdfplumber.open(file_path, password=password) as pdf:
                
                for page in pdf.pages:
                    table = page.extract_table(table_settings)
                    pages.append(table)
                    
            return pages
        except PDFPasswordIncorrect as e:
            raise InvalidPasswordException("Incorrect password, Please provide correct password.") from e

        except PDFSyntaxError as e:
            raise CorruptedPdfException("Passed pdf file is corrupted.") from e

        except Exception as e:
            logger.exception(e)
            raise StatementReaderException(f"Unexpected error while parsing {e}") from e
        