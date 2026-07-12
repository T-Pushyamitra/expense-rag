class StatementReaderException(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidPasswordException(StatementReaderException):
    pass


class UnsupportedFileException(StatementReaderException):
    pass

class CorruptedPdfException(StatementReaderException):
    pass