from src.app.plugins import db
import re


class Serializer:
    data = None
    validation = None
    errors = {}

    def __init__(self, data, validation):
        self.data = data
        self.validation = validation
        self.errors = {}

    def validate(self, data, validation, parent_key=None):
        for item in validation:
            if parent_key:
                key = f'{parent_key}.{item}'
            else:
                key = item

            if type(validation[item]) != str:
                self.validate(data.get(item, None), validation[item], key)
            elif self.passed_validation(data.get(item, None), validation[item]):
                self.errors[key] = self.passed_validation(data.get(item, None), validation[item])

        if len(self.errors):
            return False

        return True

    def is_valid(self):
        return self.validate(self.data, self.validation)

    def passed_validation(self, item, rule):
        rules = rule.split('|')
        errors = []

        if 'required' in rules and not item:
            return ['Required field']

        if 'str' in rules and type(item) != str:
            return ['Need to be a string']

        if 'int' in rules and type(item) != str:
            return ['Need to be an integer']

        if 'email' in rules:
            email_regex = re.compile("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$")

            if not email_regex.match(item):
                return [f'{"Incorrect email format"}']

        for rule in rules:
            error = self.apply_rule(rule, item)

            if error:
                errors.append(error)

        if len(errors):
            return errors

        return []

    @staticmethod
    def apply_rule(rule, item):
        if rule.startswith("min"):
            try:
                value = rule.split(":")[1]
                if len(item) < int(value):
                    return f'Length should be more then {value}'
            except Exception as e:
                print(e)
                return False
        elif rule.startswith("max"):
            try:
                value = rule.split(":")[1]
                if len(item) > int(value):
                    return f'Length should be less then {value}'
            except Exception as e:
                print(e)
                return False
        elif rule.startswith("exact"):
            try:
                value = rule.split(":")[1]
                if len(item) != int(value):
                    return f'Length must be equal to {value}'
            except Exception as e:
                print(e)
                return False
        elif rule.startswith("exists"):
            try:
                value = rule.split(":")[1]
                table, column = value.split(',')
                result = db.engine.execute(f"SELECT COUNT(*) FROM public.{table} WHERE {column}={item}")

                for row in result:
                    if not row[0]:
                        return f"record not exits"
            except Exception as e:
                print(e)
                return False
        return False


# data = {
#     "age": 23,
#     "name": '23asf',
#     "teacher": {
#         "id": 2,
#         "model": {
#             "custom": '23',
#             "name": '23232323',
#         }
#     }
# }
#
# validation = {
#     "name": 'str|email',
#     "teacher": {
#         "name": 'str|required|min:2|max:3|email',
#         "model": {
#             "name": 'str|required|max:3|exact:55|exists:role,id'
#         }
#     }
# }
#
# serializer = Serializer(data, validation)
#
# if not serializer.is_valid():
#     print(serializer.errors)
