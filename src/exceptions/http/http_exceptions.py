class ValidationException(Exception):
    def __init__(self, errors=None, message=None):
        self.errors = errors
        self.message = message


class UnknownException(Exception):
    def __init__(self, exception=None, message=None):

        if message:
            self.message = message

        if exception:
            self.exception = exception


class NotFoundException(Exception):
    message = None

    def __init__(self, message=None):
        if message:
            self.message = message
