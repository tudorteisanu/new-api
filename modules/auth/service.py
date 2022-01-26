from flask import request
from modules.users.models import User
from modules.users.schema import UserSchema
from flask_restful import Resource
from flask_login import login_user, logout_user
from modules.auth.serializer import LoginSerializer
from json import loads


class LoginResource(Resource):
    @staticmethod
    def post():
        data = request.json or request.form or loads(request.data)

        serializer = LoginSerializer(data)

        if not serializer.is_valid():
            return serializer.errors, 422

        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return {"message": 'User not found'}, 404

        if user.check_password(data['password']):
            login_user(user)
            user_data = UserSchema(exclude=['password_hash']).dump(user)
            user_data['token'] = user.create_token()
            return user_data, 200

        return {'message': "user not found"}, 401


class LogoutResource(Resource):
    @staticmethod
    def post():
        logout_user()
        return {"message": "success"}, 200


