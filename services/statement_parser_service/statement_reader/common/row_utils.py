import re


def normalize_row(row: list[str], join_only: bool = True, remove_digits: bool = False) -> str:
    """
    Normalize a row using regex.
    Args:
        row: pass row from statement reader instance
        join_only: make it True only if you want to join rows (Default: True)
        remove_digits: make it True only if you want to remove digits

    Returns:

    """
    text = "".join(row)

    if not remove_digits and join_only:
        return text

    text = text.lower()

    if remove_digits:
        # Remove symbols and digits
        return re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove only symbols
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def clean_rows(rows: list[str]) -> list[str]:
    return [row for row in rows if row]


def contains(row: list[str], pattern):
    if isinstance(pattern, list):
        return any(k.lower() in normalize_row(row) for k in pattern)

    if isinstance(pattern, str):
        return re.search(pattern, normalize_row(row, join_only=True)) is not None

    raise TypeError("pattern must be a list[str] or a regex string")

def is_bad_row(row: list, bad_keywords: list) -> bool:
    """
    Check if any bad keywords present
    Args:
        row (List): pass a transaction row from statement reader instance
        bad_keywords (list): pass list of keywords which consider a row as bad.
    Returns:
        bool: returns true if any one keyword is present
            Examples:
        >>> good_row = [
        ...     "01/01/24",
        ...     "UPI PAYMENT",
        ...     "500.00",
        ...     "1500.00"
        ... ]
        >>> is_bad_row(good_row, ['closing', 'account'])
        False
        >>> bad_row = ["closing balance", "1234", "", ""]
        >>> is_bad_row(bad_row, ['closing', 'account'])
        True
    """
    return contains(row, bad_keywords)


def is_transaction_row(row: list, regex: str) -> bool:
    """
    Check if given regex patter is found in row.
    If the regex is found in the row it is considered as start of transaction row
    Args:
        row (list): pass a transaction row from statement reader instance
        regex (str): pattern to find in the row
    Returns:
        bool: return true if pattern is found
    Examples:
        >>> good_row = [
        ...     "01/01/24",
        ...     "UPI PAYMENT",
        ...     "500.00",
        ...     "1500.00"
        ... ]
        >>> is_transaction_row(good_row, r"\\d{2}/\\d{2}/\\d{2}")
        True
        >>> bad_row = ["closing balance", "1234", "", ""]
        >>> is_bad_row(bad_row, ['closing', 'account'])
        False
    """
    return contains(row, regex)

def is_row_empty(row: list) -> bool:
    """
    Check if row is empty
    Args:
        row (list): pass a transaction row from statement reader instance
    Returns:
        bool: return true if all the items in list if empty string
    """
    if row is None or len(row) == 0:
        return True
    if all(x is None or (isinstance(x, str) and x.strip() == "") for x in row):
        return True
    return False
