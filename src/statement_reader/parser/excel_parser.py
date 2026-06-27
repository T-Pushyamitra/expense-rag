from .parser_abstract import Parser

class ExcelParser(Parser):
    def __init__(self, name: str) -> None:
         super().__init__(name)
    
    def parse(self, file_path: str, password: str) -> None:
        # TODO: replace this stub with actual Excel extraction logic
        return f"Excel content for {file_path} (password={password})"


         