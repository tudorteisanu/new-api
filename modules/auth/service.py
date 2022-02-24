# utf-8
import logging

from flask import request, url_for
from flask import redirect
from flask_restful import Resource
from flask_login import logout_user, login_user
from datetime import datetime, timedelta
from flask_login import current_user
from flask import g

from config.flask_config import FlaskConfig
from config.settings import db
from config.settings import login_manager

from services.auth_utils import auth_required
from services.mail.mail import send_email_link
from services.mail.mail import send_forgot_password_email
from services.mail.mail import send_info_email
from services.mail.token import generate_confirmation_token, confirm_token

from modules.users.models import User
from modules.users.repository import userRepository

from modules.auth.serializer import LoginSerializer
from modules.auth.serializer import RegisterSerializer
from modules.auth.serializer import ChangePasswordSerializer
from modules.auth.serializer import ForgotPasswordSerializer
from modules.auth.serializer import ResetPasswordSerializer
from modules.auth.serializer import ConfirmEmailSerializer
from modules.auth.serializer import CheckResetTokenSerializer

from services.HttpErrors import UnprocessableEntity
from services.HttpErrors import NotFound
from services.HttpErrors import UnauthorizedError
from services.HttpErrors import InternalServerError
from services.HttpErrors import Success


class LoginResource(Resource):
    @staticmethod
    def post():
        data = request.json
        serializer = LoginSerializer(data)

        if not serializer.is_valid():
            return UnprocessableEntity(errors=serializer.errors)

        user = userRepository.find_one(email=data['email'])

        if not user:
            return NotFound()

        if user.login_blocked_time:
            if user.login_blocked_time > datetime.now():
                difference = user.login_blocked_time - datetime.now()
                message = f"Возможность входа в аккаунт временно заблокированно. Осталось времени блокировки: {parse_minutes(difference.seconds)}."
                return UnprocessableEntity(message=message)
            else:
                user.update({
                    "login_attempts": 3,
                    "login_blocked_time": None
                })

        if user.check_password(data['password']):
            if not user.confirmed_at:
                return UnprocessableEntity(message='User not confirmed')

            if not user.is_active:
                return NotFound()

            user.create_token()
            login_user(user)

            if user.login_attempts != 3:
                userRepository.update(user, {
                    "login_attempts": 3
                })

            if user.reset_password_at:
                userRepository.update(user, {
                    "reset_password_at": None,
                    "reset_code": None
                })

            db.session.commit()

            response = {
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                },
                "token": user.token.access_token
            }

            return Success(data=response)
        else:
            user.login_attempts = user.login_attempts - 1

            if user.login_attempts == 0:
                user.login_blocked_time = datetime.now() + timedelta(minutes=15)
            message = f"Вы ввели неверны пароль. Возможные попытки: {user.login_attempts}, по истечению которых, ваш аккаунт будет временно заблокирован"
            db.session.commit()
            return UnprocessableEntity(message=message)


class RegisterResource(Resource):
    @staticmethod
    def post():
        try:
            data = request.json
            serializer = RegisterSerializer(data)

            if not serializer.is_valid():
                return UnprocessableEntity(serializer.errors)

            if userRepository.find_one(email=data['email']) is not None:
                return UnprocessableEntity(message="User exists")

            new_user = User(
                email=data['email'],
                name=data['name'],
            )

            userRepository.create(new_user)

            new_user.hash_password(data['password'])
            new_user.create_access_token()

            token = generate_confirmation_token(new_user.email)

            send_email_link(new_user.email,
                            f'{FlaskConfig.FRONTEND_ADDRESS}/auth/email-confirmed?token={token}',
                            new_user.name)

            response = {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }

            db.session.commit()
            return Success(data=response)
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()


class ConfirmEmailResource(Resource):
    @staticmethod
    def get():
        try:
            data = request.args
            serializer = ConfirmEmailSerializer(data)

            if not serializer.is_valid():
                return serializer.errors, 422

            token = data.get('token', None)
            email = confirm_token(token)

            if not email:
                return UnprocessableEntity(message='Invalid token')

            user = User.find_one(email=email)

            if user.confirmed_at:
                return NotFound()

            user.update({
                "confirmed_at": datetime.now().isoformat(),
                "is_active": True
            })

            send_info_email(**{
                "subject": 'Email confirmed',
                "message": "Ваш email успешно подтвержден!",
                "recipient": user.email,
                "name": user.name
            })

            return Success()

        except Exception as e:
            print(e)
            return InternalServerError()


class ReadUserResource(Resource):
    @staticmethod
    def get(user_id):
        try:
            return Success()
        except Exception as e:
            print(e)
            return InternalServerError()


class LogoutResource(Resource):
    @staticmethod
    @auth_required()
    def post():
        try:
            user = userRepository.get(current_user.id)
            user.remove_token()
            logout_user()
            db.session.commit()
            return Success()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return UnauthorizedError()


class ForgotPasswordResource(Resource):
    @staticmethod
    def post():
        data = request.json
        serializer = ForgotPasswordSerializer(data)

        if not serializer.is_valid():
            return serializer.errors, 422

        user = userRepository.find_one(email=data.get('email'))

        if not user:
            return NotFound()

        if user.reset_password_at is not None and user.reset_password_at > datetime.now():
            difference = user.reset_password_at - datetime.now()
            time = parse_minutes(difference.seconds)
            message = f"Вы уже запросили ссылку на восстановление пароля. Сможете отправить повторно через {time}"
            return UnprocessableEntity(message=message)

        token = generate_confirmation_token(user.email)

        send_forgot_password_email(user.email,
                                   f'{FlaskConfig.FRONTEND_ADDRESS}/reset_password?token={token}',
                                   user.name)

        userRepository.update(user,
                              {
                                  "reset_code": token,
                                  "reset_password_at": datetime.now() + timedelta(minutes=5)
                              }
                              )
        db.session.commit()
        return Success()


class CheckResetTokenResource(Resource):
    @staticmethod
    def post():
        data = request.json

        serializer = CheckResetTokenSerializer(data)

        if not serializer.is_valid():
            return serializer.errors, 422

        token = data.get('token', None)
        email = confirm_token(token)

        if not email:
            return UnprocessableEntity(message='Invalid token')

        user = User.find_one(email=email)

        if not user or not user.reset_code or user.reset_code != token:
            return UnprocessableEntity(message='Invalid token')

        return Success()


class ResetPasswordResource(Resource):
    @staticmethod
    def post():
        try:
            data = request.json
            serializer = ResetPasswordSerializer(data)

            if not serializer.is_valid():
                return serializer.errors, 422

            password = data.get('password', None)
            token = data.get('token', None)
            email = confirm_token(token)

            if not email:
                return UnprocessableEntity(message='Invalid token')

            user = User.find_one(email=email)

            if not user or not user.reset_code or user.reset_code != token:
                return UnprocessableEntity(message='Invalid token')

            user.hash_password(password)
            user.update({"reset_code": None, "is_active": True})
            send_info_email(**{
                "subject": 'Аккаунт успешно востоновлен!',
                "message": "Ваш Аккаунт успешно востоновлен!",
                "recipient": user.email,
                "name": user.name
            })
            return Success
        except Exception as e:
            print(e)
            return InternalServerError()


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
            return UnprocessableEntity('Passwords don\'t much')

        user = User.query.get(current_user.id)

        if not user:
            return NotFound()

        if not user.check_password(old_password):
            return UnprocessableEntity(message='Invalid password')

        if old_password == new_password:
            return UnprocessableEntity(message='Old password and new password should be different')

        user.hash_password(new_password)

        send_info_email(**{
            "subject": 'Изменение пароля!',
            "message": "Ваш пароль успешно изменен!",
            "recipient": user.email,
            "name": user.name
        })
        return Success()


def parse_minutes(seconds):
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
