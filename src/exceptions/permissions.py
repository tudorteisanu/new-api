class Error(Exception):
    """Base class for other exceptions"""
    pass


class PermissionsException(Error):
    def __init__(self, message):
        self.message = message
