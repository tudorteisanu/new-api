class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class UnknownError(Exception):
    def __init__(self):
        pass
