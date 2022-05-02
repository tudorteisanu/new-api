class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class UnknownError(Exception):
    def __init__(self, exception):
        return exception


class NotFoundException(Exception):
    message = None

    def __init__(self, message):
        if message:
            self.message = message

