from .parser_abstract import Parser
import pdfplumber
import logging

logger = logging.getLogger("my_project")

class PDFParser(Parser):
    def __init__(self) -> None:
        super().__init__("PDF Parser")

    def parse(self, file_path: str, password: str, debug: bool = False):
        table_settings = {
              "vertical_strategy": "text",
    "horizontal_strategy": "text",
    "min_words_vertical": 2,
    "min_words_horizontal": 1,
    "snap_tolerance": 5,
    "join_tolerance": 5,
    "intersection_tolerance": 5,
    "text_x_tolerance": 2,
    "text_y_tolerance": 3,
        }

        total_tables = 0
        total_rows = 0
        with pdfplumber.open(file_path, password=password) as pdf:
            for i, page in enumerate(pdf.pages):
                if debug:
                    print(f"Extracting tables from page {i + 1}...")
                table = page.find_table(table_settings)
                table = page.extract_table(table_settings)
                if not table:
                    continue

                total_tables += 1
                for row in table:
                    total_rows += 1
                    yield row

        logger.info(f"Extracted {total_tables} tables and {total_rows} non-empty rows from the PDF.")
    
    def get_last_page(self, file_path: str, password: str, debug: bool = False):
        table_settings = {
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "min_words_vertical": 2,
                "min_words_horizontal": 1,
                "snap_tolerance": 5,
                "join_tolerance": 5,
                "intersection_tolerance": 5,
                "text_x_tolerance": 2,
                "text_y_tolerance": 3,
            }
        with pdfplumber.open(file_path, password=password) as pdf:
            last_page = pdf.pages[-1]
            table = last_page.extract_table(table_settings)
            return table
        