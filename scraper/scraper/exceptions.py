class ExpectedValueMissingException(Exception):
    """Raised when during scraping a value was expected but was not found"""
    pass

class InputMissingException(Exception):
    """Raised when a program needs some input which is missing. For example environmental variable"""
    pass