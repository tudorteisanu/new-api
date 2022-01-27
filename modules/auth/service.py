from flask import request
from modules.users.models import User
from modules.users.schema import UserSchema
from flask_restful import Resource
from flask_login import login_user, logout_user
from modules.auth.serializer import LoginSerializer
from modules.auth.serializer import RegisterSerializer
from modules.auth.serializer import ChangePasswordSerializer
from config.settings import db
from config.settings import login_manager
from flask_jwt_extended import decode_token
from datetime import datetime
from flask_login import current_user
from services.auth_utils import auth_required


class LoginResource(Resource):
    @staticmethod
    def post():
        data = request.json

        serializer = LoginSerializer(data)

        if not serializer.is_valid():
            return serializer.errors, 422

        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return {"message": 'User not found'}, 404

        if user.check_password(data['password']):
            login_user(user)
            user.create_token()
            user_data = UserSchema(only=['name', 'id', 'token', 'role', 'email']).dump(user)
            db.session.commit()
            user_data['token'] = user_data['token']['access_token']
            return user_data, 200
        else:
            return {'message': "Invalid password"}, 422


class RegisterResource(Resource):
    @staticmethod
    def post():
        data = request.json
        serializer = RegisterSerializer(data)

        if not serializer.is_valid():
            return serializer.errors, 422

        user = User.query.filter_by(email=data['email']).first()

        if user is not None:
            return {'message': 'user_exists'}, 401

        user = User(
            name=data['name'],
            email=data['email'],
        )

        db.session.add(user)
        db.session.commit()

        user.hash_password(data['password'])

        user.create_access_token()

        if data and data.get('role', None) is not None:
            user.role = data['role']

        db.session.commit()
        return UserSchema(only=['id', 'name', 'email', 'role']).dump(user)


class LogoutResource(Resource):
    @staticmethod
    def post():
        try:
            user = User.query.get(current_user.id)
            user.remove_token()
            logout_user()
            return {"message": "success"}, 200
        except:
            return {"message": "Unauthorized"}, 401


class ForgotPasswordResource(Resource):
    @staticmethod
    def post():
        data = request.json
        if not data:
            return {"message": 'Email is required'}, 422

        email = data.get('email', None)

        if not email:
            return {"message": 'Email is required'}, 422

        user = User.query.filter_by(email=email).first()

        if not user:
            return {'message': 'User not found'}, 404

        user.generate_reset_password_code()
        db.session.commit()
        return {'message': 'success'}, 200


class CheckResetTokenResource(Resource):
    @staticmethod
    def post():
        data = request.json

        if not data or not data.get('token', None):
            return {'message': 'Reset code is required'}, 400

        user = User.query.filter_by(reset_code=data.get('token', None)).first()
        if not user:
            return {}
        return {'message': 'success'}, 200


class ResetPasswordResource(Resource):
    @staticmethod
    def post():
        data = request.json
        password = data.get('password', None)
        reset_code = data.get('token', None)

        if not reset_code:
            return {'message': 'Reset code is required'}, 400

        user = User.query.filter_by(reset_code=reset_code).first()

        if not user:
            return {'message': 'User not found'}, 404
        user.hash_password(password)
        user.remove_expired_token()
        db.session.commit()
        return {'message': 'success'}, 200


class ChangePasswordResource(Resource):
    @staticmethod
    @auth_required()
    def post():
        data = request.json
        serializer = ChangePasswordSerializer(data)

        if not serializer.is_valid():
            return serializer.errors, 422

        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)
        password_confirmation = data.get('password_confirmation', None)

        if new_password != password_confirmation:
            return {'message': 'Passwords don\'t much'}, 404

        user = User.query.get(current_user.id)

        if not user:
            return {'message': 'User not found'}, 404

        if not user.check_password(old_password):
            return {'message': 'Invalid password'}, 404

        if old_password == new_password:
            return {'message': 'Old password and new password should be different'}, 404

        user.hash_password(new_password)
        db.session.commit()
        return {'message': 'success'}, 200


@login_manager.request_loader
def load_user_from_request(flask_request):
    if flask_request.headers.get('Authorization', None):
        access_token = flask_request.headers.get('Authorization').split(' ')[1]
        token = decode_token(access_token)
        token_expiry = datetime.fromtimestamp(token['exp'])

        if token_expiry < datetime.now():
            logout_user()
            return None

        user = User.query.get(token['identity'])

        if not user or not user.token.access_token or user.token.access_token != access_token:
            return None

        return user
    return None
