from src.services.serializer.utils.primitives import IsString
from inspect import isclass


class Base:
    __abstract__ = True
    errors = {}
    data = None
    String = IsString()

    @classmethod
    def validate(cls, obj, key=None, index=None):
        for item in obj.__dict__:
            if not item.startswith("__") and not item.endswith("__") and item != 'data' and item != 'errors':
                field = item
                attr = getattr(obj, item)

                if index is not None:
                    if key is not None:
                        field = f'{key}.{index}.{item}'

                elif key is not None:
                    field = f'{key}.{item}'

                if not isclass(attr):
                    if attr.required:
                        has_error = False

                        if obj.data is None and attr.required:
                            cls.errors[field] = ['Required field']

                        if hasattr(attr, "is_list") and attr.is_list:
                            if obj.data.get(item, None) is None and attr.required:
                                cls.errors[field] = ['Required field']
                            elif type(obj.data.get(item, None)) != list:
                                cls.errors[field] = ['Must be a list of items']
                            return

                        if type(obj.data) == dict:
                            if obj.data.get(item, None) is None:
                                has_error = True
                            elif type(obj.data[item]) == list and len(obj.data[item]) == 0 or not obj.data[item]:
                                has_error = True
                        elif (type(obj.data) == str or type(obj.data) == int) and not obj.data:
                            has_error = True

                        if has_error:
                            cls.errors[field] = ['this is Required field']



                    if attr and hasattr(attr, 'is_list') and getattr(attr, 'is_list'):
                        if hasattr(attr, 'serializer'):
                            serializer = getattr(attr, 'serializer')

                            if obj.data.get(item, None) is None:
                                return

                            for idx, el in enumerate(obj.data[item]):
                                child = serializer
                                if not child:
                                    return
                                setattr(child, "data", el)
                                cls.validate(child, field, index=idx)

                    elif attr and type(obj.data) == dict and obj.data.get(item, None) and attr(obj.data[item]):
                        cls.errors[field] = attr(obj.data[item])
                else:
                    child = attr

                    if obj.data.get(item, None) is None:
                        cls.errors[field] = ['this is Required field']
                        return

                    setattr(child, "data", obj.data[item])
                    cls.validate(child, field)

    @classmethod
    def is_valid(cls):
        cls.errors = {}
        cls.validate(cls)
        return len(cls.errors) == 0

    @classmethod
    def __call__(cls):
        cls.errors = {}

    @classmethod
    def __init__(cls, data):
        cls.data = data
