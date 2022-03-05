class IsString:
    def __init__(self, min_length=None, max_length=None, required=False, message=None):
        self.message = message
        self.min_length = min_length
        self.max_length = max_length
        self.required = required

    def __call__(self, data):
        messages = []

        if type(data) != str:
            message = f'Field must be a string!'
            messages.append(message)
        else:
            if self.min_length is not None and len(data) < self.min_length:
                message = f'Length must be more than {self.min_length}!'
                messages.append(message)

            elif self.max_length is not None and len(data) > self.max_length:
                message = f'Length must be less than {self.max_length}!'
                messages.append(message)

        if len(messages):
            return messages
        return False


class IsNumber:
    def __init__(self, min_value=None, max_value=None, required=False, message=None):
        self.message = message
        self.min_value = min_value
        self.max_value = max_value
        self.required = required

    def __call__(self, data):
        messages = []

        if type(data) != int:
            message = f'Field must be an integer!'
            messages.append(message)
        else:
            if self.min_value is not None and data < self.min_value:
                message = f'Value must be more than {self.min_value}!'
                messages.append(message)

            elif self.max_value is not None and data > self.max_value:
                message = f'Value must be less than {self.max_value}!'
                messages.append(message)

        if len(messages):
            return messages
        return False


class IsEnum:
    def __init__(self, items=[], required=False, message=None):
        self.message = message
        self.items = items
        self.required = required

    def __call__(self, data):
        messages = []

        if data not in self.items:
            message = f'Invalid value!'
            messages.append(message)

        if len(messages):
            return messages
        return False


class IsList:
    is_list = True

    def __init__(self, required=False, serializer=None, message=None):
        self.message = message
        self.serializer = serializer
        self.required = required

    def __call__(self, data):
        messages = []

        if type(data) != list:
            message = f'Must be a list!'
            messages.append(message)

        if len(messages):
            return messages
        return False

