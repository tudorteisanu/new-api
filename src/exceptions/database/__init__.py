class SqlException(Exception):
    def __init__(self, exception):
        if exception:
            self.exception = exception
