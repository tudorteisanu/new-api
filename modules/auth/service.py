from flask import request
from modules.users.models import User
from modules.users.schema import UserSchema
from flask_restful import Resource
from flask_login import login_user, logout_user
from modules.auth.serializer import LoginSerializer
from json import loads
from config.settings import app, db
from flask import render_template
from helpers.auth_utils import auth_required


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


class RegisterResource(Resource):
    @staticmethod
    def post():
        data = request.json or request.form or loads(request.data)

        current_user = User.query.filter_by(email=data['email']).first()
        if current_user is not None:
            return {'message': 'user_exists'}, 401

        elif current_user is None:
            user = User(
                name=data['name'],
                email=data['email'],
            )

            user.hash_password(data['password'])

            if data and data.get('role', None) is not None:
                user.role = data['role']

            db.session.add(user)
            db.session.commit()
            return UserSchema(only=['id', 'name', 'email', 'role']).dump(user)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/')
# @auth_required()
def index():
    return render_template('index.html')
