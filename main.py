from src.statement_reader.hdfc_statement_reader import HDFCStatementReader
from src.statement_reader.axis_statement_reader import AxisStatementReader

from src.config.logging import setup_logger
import logging
from os.path import join

setup_logger()

logger = logging.getLogger("exepnse-rag")

# hdfc_file_path = join("resources", "statements", "hdfc_bank.pdf")
# bank = HDFCStatementReader(hdfc_file_path, "201150838")
# bank.reader()

# print(len(bank.transactions))

axis_file_path = join("resources", "statements", "axis_bank_statement.pdf")
bank = AxisStatementReader(axis_file_path)
bank.reader()

print("AXIS BANK")
for i in bank.transactions:
    logger.info(i)
