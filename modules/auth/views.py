from config.settings import db
from modules.users.models import User
from modules.users.schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, g
from helpers.auth_utils import auth_required
from helpers.send_standart_message import send_message
import random


def send_email_link(email, link):
    body = f'{link}'
    send_message('Reset password', body=body)


class AuthRoute:
    @staticmethod
    def register():
        data = request.args
        current_user = User.query.filter_by(email=data['email']).first()
        if current_user is not None:
            return jsonify({'message': 'user_exists'}), 401

        elif current_user is None:
            user = User(
                name=data['name'],
                email=data['email'],
                password_hash=generate_password_hash(data['password'])
            )

            if data and data.get('role', None) is not None:
                user.role = data['role']
            db.session.add(user)
            db.session.commit()
            return jsonify(UserSchema(only=['id', 'name', 'email', 'role']).dump(user))

    @staticmethod
    def reset_password_step_1():
        data = request.args

        email = data.get('email', None)

        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                hash = random.getrandbits(128)
                link = f'http://localhost://5000/reset={hash}'
                user.reset_code = hash
                send_email_link(email, link)

    @staticmethod
    def reset_password_step_2():
        pass

    @staticmethod
    def reset_password_step_3():
        pass

    @staticmethod
    @auth_required()
    def change_password():
        data = request.json

        if check_password_hash(g.user.password_hash, data['password']):
            return jsonify({'message': "The new password must not be the same as the old one"}), 422
        else:
            user = User.query.get(g.user.id)
            user.password_hash = generate_password_hash(data['password'])
