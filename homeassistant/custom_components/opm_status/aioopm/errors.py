class AioopmException(Exception):
    """Base error for aioopm"""


class RequestError(AioopmException):
    """Unable to fulfill request.

    Raised when host or API cannot be reached.
    """
