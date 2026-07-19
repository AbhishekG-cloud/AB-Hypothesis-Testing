import sys


import sys


def error_message_detail(error: Exception, error_details: sys) -> str:
    """
    Generate a detailed error message containing the source file,
    line number, and the original exception message.

    This function extracts traceback information from the provided
    exception details (typically the `sys` module) using `exc_info()`.
    It is commonly used in custom exception handling to provide more
    informative error messages for debugging.

    Args:
        error (Exception):
            The exception object that was raised.
        error_details (sys):
            The Python `sys` module, used to retrieve the current
            exception's traceback via `sys.exc_info()`.

    Returns:
        str:
            A formatted string containing:
            - The filename where the exception occurred.
            - The line number that raised the exception.
            - The original exception message.

    Example:
        >>> import sys
        >>> try:
        ...     x = 10 / 0
        ... except Exception as e:
        ...     print(error_message_detail(e, sys))
        Error occurred in python script [/path/to/file.py]
        at line number [15]
        error message [division by zero]

    Notes:
        - This function should be called inside an `except` block,
          otherwise `sys.exc_info()` will return `(None, None, None)`.
        - The returned message is intended for logging and debugging
          purposes rather than displaying directly to end users.
    """
    _, _, exc_tb = error_details.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = (
        "Error occurred in python script [{0}] "
        "at line number [{1}] "
        "error message [{2}]"
    ).format(file_name, exc_tb.tb_lineno, str(error))

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_details)

    def __str__(self):
        return self.error_message


class InvalidInputError(ValueError):
    """Raised when user input is invalid."""

    pass
