# utf-8
from flask import request, url_for
from flask import redirect
from flask_restful import Resource
from flask_login import logout_user, login_user
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
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

from modules.users.models import UserResource as User
from modules.users.schema import UserSchema

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


class BaseResource(Resource):
    __abstract__ = True
    auth = False

    def __init__(self):
        if self.auth:
            verify_jwt_in_request()
            load_user(get_jwt_identity())


class LoginResource(BaseResource):
    @staticmethod
    def post():
        data = request.json
        serializer = LoginSerializer(data)

        if not serializer.is_valid():
            return UnprocessableEntity(errors=serializer.errors)

        user = User.find_one(email=data['email'])

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
            user_data = UserSchema(only=['name', 'id', 'token', 'role', 'email']).dump(user)
            login_user(user)
            db.session.commit()

            if user.login_attempts != 3:
                user.update({
                    "login_attempts": 3
                })

            if user.reset_password_at:
                user.update({
                    "reset_password_at": None,
                    "reset_code": None
                })

            return {'user': user_data, "token": user.token.access_token}, 200
        else:
            user.update({
                "login_attempts": user.login_attempts - 1
            })

            if user.login_attempts == 0:
                user.update({
                    "login_blocked_time": datetime.now() + timedelta(minutes=15)
                })
            message = f"Вы ввели неверны пароль. Возможные попытки: {user.login_attempts}, по истечению которых, ваш аккаунт будет временно заблокирован"
            return UnprocessableEntity(message=message)


class RegisterResource(BaseResource):
    @staticmethod
    def post():
        data = request.json
        serializer = RegisterSerializer(data)

        if not serializer.is_valid():
            return serializer.errors, 422

        if User.find_one(email=data['email']) is not None:
            return UnauthorizedError(message="User exists")

        user = create(data)
        user.hash_password(data['password'])
        user.create_access_token()
        token = generate_confirmation_token(user.email)
        send_email_link(user.email,
                        f'{FlaskConfig.FRONTEND_ADDRESS}/auth/email-confirmed?token={token}',
                        user.name)
        return UserSchema(only=['id', 'name', 'email', 'role']).dump(user)


class ConfirmEmailResource(BaseResource):
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


class ReadUserResource(BaseResource):
    @staticmethod
    def get(user_id):
        try:
            return Success(data=UserSchema().dump(User.get(user_id)))
        except Exception as e:
            print(e)
            return InternalServerError()


class LogoutResource(BaseResource):
    @staticmethod
    @auth_required()
    def post():
        try:
            user = User.get(current_user.id)
            user.remove_token()
            logout_user()
            return Success()
        except Exception as e:
            print(e)
            return UnauthorizedError()


class ForgotPasswordResource(BaseResource):
    @staticmethod
    def post():
        data = request.json
        serializer = ForgotPasswordSerializer(data)

        if not serializer.is_valid():
            return serializer.errors, 422

        user = User.find_one(email=data.get('email'))

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

        user.update(
            {"reset_code": token, "reset_password_at": datetime.now() + timedelta(minutes=5)})
        return Success()


class CheckResetTokenResource(BaseResource):
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


class ResetPasswordResource(BaseResource):
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


class ChangePasswordResource(BaseResource):
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

        user = User.get(current_user.id)

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
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
