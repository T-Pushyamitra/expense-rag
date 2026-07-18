import logging
import sys


def setup_logger():

    logger = logging.getLogger("exepnse-rag")

    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Do not pass logs to root logger
    logger.propagate = False

    return logger
