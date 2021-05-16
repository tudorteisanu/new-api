from functools import wraps
from flask import request, jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, decode_token
from apps.users.models import User


def auth_required():
    def f1(fn):
        @wraps(fn)
        def f2(*args, **kwargs):
            verify_jwt_in_request()
            user = User.query.get(get_jwt_identity())
            
            if not user:
                resp = jsonify({"message": "User does not exist"})
                resp.status = "401"
                return resp
            
            token = request.headers.get("Authorization")
            # dekoded_token = decode_token(token)
            
            # role = dekoded_token['user_claims'].get('role')
            #
            # if user.role != role:
            #     resp = jsonify({"msg": "invalid role"})
            #     resp.status = "401"
            #     return resp
            
            if user.platform != request.user_agent.platform or user.browser != request.user_agent.browser:
                resp = jsonify({"msg": "your bad!"})
                resp.status = "401"
                return resp
            
            if user.token != token :
                resp = jsonify({"msg": "Bad token"})
                resp.status = "401"
                return resp
            
            if user:
                g.user = user
            
            return fn(*args, **kwargs)
        
        return f2
    
    return f1
