from functools import wraps
from flask import request
from flask_jwt_extended import decode_token
from modules.users.models import UserResource
from datetime import datetime
from flask import g


def auth_required():
    def f1(fn):
        @wraps(fn)
        def f2(*args, **kwargs):
            try:
                if request.headers.get('Authorization', None):
                    access_token = request.headers.get('Authorization').split(' ')[1]
                    token = decode_token(access_token)
                    token_expiry = datetime.fromtimestamp(token['exp'])

                    if token_expiry < datetime.now():
                        return None

                    user = UserResource.get(token['identity'])

                    if not user or not user.is_active or not user.token.access_token or user.token.access_token != access_token:
                        return {"message": "Unauthorized"}, 401

                    g.user = user

            except Exception as e:
                print(e)
                return {"message": "Invalitd token"}, 401
            return fn(*args, **kwargs)
        return f2
    return f1
