from functools import wraps
from flask_login import current_user


def auth_required():
    def f1(fn):
        @wraps(fn)
        def f2(*args, **kwargs):
            if not current_user or not current_user.is_authenticated:
                return {"message": "Unauthorized"}, 401
            return fn(*args, **kwargs)
        return f2
    return f1
