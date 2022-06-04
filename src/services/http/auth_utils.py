import logging
from functools import wraps
from flask import request
from flask_jwt_extended import decode_token
from datetime import datetime
from flask import g

from src.modules.users.models import User


def auth_required():
    def f1(fn):
        @wraps(fn)
        def f2(*args, **kwargs):
            try:
                if request.headers.get('Authorization', None) is not None:
                    access_token = request.headers.get('Authorization').split(' ')[1]
                    token = decode_token(access_token)

                    token_expiry = datetime.fromtimestamp(token['exp'])

                    if token_expiry < datetime.now():
                        return {"message": "Unauthorized"}, 401

                    user = User.query.get(token['sub'])

                    if not user or not user.is_active or not user.token.access_token \
                            or user.token.access_token != access_token:
                        return {"message": "Unauthorized"}, 401

                    g.user = user
                    request.__setattr__('user', user)
                else:
                    return {"message": "Unauthorized"}, 401

            except Exception as e:
                logging.error(e)
                return {"message": "Invalid token"}, 401
            return fn(*args, **kwargs)
        return f2
    return f1
