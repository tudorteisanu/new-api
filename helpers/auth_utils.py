from functools import wraps
from flask import jsonify
from flask_login import current_user


def auth_required():
    def f1(fn):
        @wraps(fn)
        def f2(*args, **kwargs):
            if not current_user or not current_user.is_authenticated:
                resp = jsonify({"message": "Unauthenticated"})
                resp.status = "401"
                return resp
            return fn(*args, **kwargs)
        return f2
    return f1
