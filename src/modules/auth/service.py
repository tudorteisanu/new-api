# utf-8
import logging
from flask import request
from datetime import datetime, timedelta
from flask import g
from src.app import FlaskConfig
from src.app import db

from src.services.mail.mail import send_email_link
from src.services.mail.mail import send_forgot_password_email
from src.services.mail.mail import send_info_email
from src.services.mail.token import generate_confirmation_token, confirm_token

from src.modules.users.repository import UserRepository
from src.modules.roles.repository import RoleRepository

from .serializer import LoginSerializer
from .serializer import RegisterSerializer
from .serializer import ChangePasswordSerializer
from .serializer import TokenSerializer
from .serializer import ResetPasswordSerializer
from .serializer import ForgotPasswordSerializer

from src.services.http.errors import UnprocessableEntity
from src.services.http.errors import NotFound
from src.services.http.errors import UnauthorizedError
from src.services.http.errors import InternalServerError
from src.services.http.errors import Success
from src.services.localization import Locales
from ...exceptions.http import ValidationError, UnknownError


class AuthService:
    def __init__(self):
        self.repository = UserRepository()
        self.role_repository = RoleRepository()
        self.request = request
        self.t = Locales()

    def login(self):
        data = self.request.json
        serializer = LoginSerializer(data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        try:
            user = self.repository.find_one(email=data['email'])

            if not user:
                return NotFound()

            if user.login_blocked_time:
                if user.login_blocked_time > datetime.now():
                    difference = user.login_blocked_time - datetime.now()
                    message = f"Возможность входа в аккаунт временно заблокированно." \
                              f" Осталось времени блокировки: {self.parse_minutes(difference.seconds)}."
                    return UnprocessableEntity(message=message)
                else:
                    self.repository.update(user, {
                        "login_attempts": 3,
                        "login_blocked_time": None
                    })

            if user.check_password(data['password']):
                if not user.confirmed_at:
                    return UnprocessableEntity(message='User not confirmed')

                if not user.is_active:
                    return NotFound()

                user.create_token()
                # login_user(user)

                if user.login_attempts != 3:
                    self.repository.update(user, {
                        "login_attempts": 3
                    })

                if user.reset_password_at:
                    self.repository.update(user, {
                        "reset_password_at": None,
                        "reset_code": None
                    })

                db.session.commit()

                response = {
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "role": {
                            "id": user.role_id,
                            "alias": user.role.alias,
                            "name": user.role.name,
                        } if user.role else None
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
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def register(self):
        try:
            data = self.request.json
            serializer = RegisterSerializer(data)

            if not serializer.is_valid():
                raise ValidationError(errors=serializer.errors)

            if self.repository.find_one(email=data['email']) is not None:
                return UnprocessableEntity(message="User exists")

            new_user = self.repository.create(
                email=data['email'],
                name=data['name'],
            )

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
        except ValidationError as e:
            raise e
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            raise UnknownError()

    def confirm_email(self):
        try:
            data = self.request.args
            serializer = TokenSerializer(data)

            if not serializer.is_valid():
                return serializer.errors, 422

            token = data.get('token', None)
            email = confirm_token(token)

            if not email:
                return UnprocessableEntity(message='Invalid token')

            user = self.repository.find_one(email=email)

            if user.confirmed_at:
                return NotFound()

            user.update(user, {
                "confirmed_at": datetime.now().isoformat(),
                "is_active": True
            })

            send_info_email(**{
                "subject": 'Email confirmed',
                "message": "Ваш email успешно подтвержден!",
                "recipient": user.email,
                "name": user.name
            })

            db.session.commit()
            return Success()

        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def read(self, user_id):
        try:
            if not g.user:
                return NotFound()

            user = self.repository.get(user_id)

            if not user:
                return NotFound(message="User not found")

            if g.user.id != user.id:
                return NotFound()

            response = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": {
                    "id": user.role_id,
                    "alias": user.role.alias,
                    "name": user.role.name,
                } if user.role else None
            }
            return Success(data=response)
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def logout(self):
        try:
            user = self.repository.find_one(id=g.user.id)
            user.remove_token()
            db.session.commit()
            return Success()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return UnauthorizedError()

    def forgot_password(self):
        try:
            data = self.request.json
            serializer = ForgotPasswordSerializer(data)

            if not serializer.is_valid():
                return serializer.errors, 422

            user = self.repository.find_one(email=data.get('email'))

            if not user:
                return NotFound()

            if user.reset_password_at is not None and user.reset_password_at > datetime.now():
                difference = user.reset_password_at - datetime.now()
                time = self.parse_minutes(difference.seconds)
                message = f"Вы уже запросили ссылку на восстановление пароля. Сможете отправить повторно через {time}"
                return UnprocessableEntity(message=message)

            token = generate_confirmation_token(user.email)

            send_forgot_password_email(user.email,
                                       f'{FlaskConfig.FRONTEND_ADDRESS}/reset_password?token={token}',
                                       user.name)

            self.repository.update(user,
                                   {
                                       "reset_code": token,
                                       "reset_password_at": datetime.now() + timedelta(minutes=5)
                                   }
                                   )
            db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def check_reset_token(self):
        try:
            data = self.request.json

            serializer = TokenSerializer(data)

            if not serializer.is_valid():
                return serializer.errors, 422

            token = data.get('token', None)
            email = confirm_token(token)

            if not email:
                return UnprocessableEntity(message='Invalid token')

            user = self.repository.find_one(email=email)

            if not user or not user.reset_code or user.reset_code != token:
                return UnprocessableEntity(message='Invalid token')

            return Success()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def reset_password(self):
        try:
            data = self.request.json
            serializer = ResetPasswordSerializer(data)

            if not serializer.is_valid():
                return serializer.errors, 422

            password = data.get('password', None)
            token = data.get('token', None)
            email = confirm_token(token)

            if not email:
                return UnprocessableEntity(message='Invalid token')

            user = self.repository.find_one(email=email)

            if not user or not user.reset_code or user.reset_code != token:
                return UnprocessableEntity(message='Invalid token')

            user.hash_password(password)
            self.repository.update(user, {"reset_code": None, "is_active": True})
            send_info_email(**{
                "subject": 'Аккаунт успешно восстановлен!',
                "message": "Ваш Аккаунт успешно восстановлен!",
                "recipient": user.email,
                "name": user.name
            })
            db.session.commit()
            return Success()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def change_password(self):
        try:
            data = self.request.json
            serializer = ChangePasswordSerializer(data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            old_password = data.get('old_password', None)
            new_password = data.get('new_password', None)
            password_confirmation = data.get('password_confirmation', None)

            if new_password != password_confirmation:
                return UnprocessableEntity('Passwords don\'t much')

            user = self.repository.get(g.user.id)

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
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    @staticmethod
    def parse_minutes(seconds):
        return f"{seconds // 60:02d}:{seconds % 60:02d}"
