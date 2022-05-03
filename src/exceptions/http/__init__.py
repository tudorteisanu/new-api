class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class UnknownError(Exception):
    def __init__(self, exception=None):
        return exception


class NotFoundException(Exception):
    message = None

    def __init__(self, message=None):
        if message:
            self.message = message

