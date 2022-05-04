class ValidationException(Exception):
    def __init__(self, errors):
        self.errors = errors


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

