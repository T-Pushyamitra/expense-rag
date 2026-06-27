from .parser_abstract import Parser

class PDFParser(Parser):
    def __init__(self) -> None:
        super().__init__("PDF Parser")

    def parse(self, file_path: str, password: str) -> None:
        # TODO: replace this stub with actual PDF extraction logic
        return f"PDF content for {file_path} (password={password})"