import logging

from ..common.statement_reader_abstract import StatementReader
from ..common.transaction_utils import Transaction
from ..parser.statement_parser_factory import StatementParserFactory
from .axis_statement_extractor import AXISStatementExtractor

logger = logging.getLogger("exepnse-rag")


class AXISStatementReader(StatementReader):
    def __init__(self, file_path: str, password: str = None, document_id: str = None):
        """
        Initializes an AXIS statement reader.

        Args:
        file_path (str): Path to the AXIS bank statement file.
        password (str, optional): Password for encrypted statement files. Defaults to None.
        document_id (str, optional): Unique identifier associated with the document. Defaults to None.
        """
        super().__init__()
        self.file_path: str = file_path
        self._password: str = password or ""
        self.document_id: str = document_id or ""

    def reader(self) -> list[Transaction]:
        """
        Reads the statement file and return Transaction object

        Returns:
            list[Transaction]:
        """
        statement_parser = StatementParserFactory.get_parser(self.file_path.split(".")[-1])

        pages = statement_parser.parse(
            self.file_path, self._password, vertical_strategy="lines", horizontal_strategy="lines"
        )

        extractor = AXISStatementExtractor(self.file_path.split(".")[-1])
        transactions = extractor.feeder(pages)
        return transactions
