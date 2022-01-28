from flask import request, url_for

from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header
from config.flask_config import FlaskConfig
from modules.users.models import User
from modules.users.schema import UserSchema
from flask_restful import Resource
from flask_login import logout_user, login_user
from modules.auth.serializer import LoginSerializer
from modules.auth.serializer import RegisterSerializer
from modules.auth.serializer import ChangePasswordSerializer
from config.settings import db, app
from config.settings import login_manager
from flask_jwt_extended import decode_token
from datetime import datetime
from flask_login import current_user
from services.auth_utils import auth_required
from services.mail.mail import send_email_link
from services.mail.mail import send_forgot_password_email
from services.mail.mail import send_info_email

from services.mail.token import generate_confirmation_token, confirm_token
from flask import redirect


class LoginResource(Resource):
    @staticmethod
    def post():
        data = request.json

        serializer = LoginSerializer(data)

        if not serializer.is_valid():
            return serializer.errors, 422

        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.is_active:
            return {"message": 'User not found'}, 404

        if user.check_password(data['password']):
            if not user.confirmed_at:
                return {'message': "User not confirmed"}, 422

            user.create_token()
            user_data = UserSchema(only=['name', 'id', 'token', 'role', 'email']).dump(user)
            db.session.commit()
            user_data['token'] = user_data['token']['access_token']
            login_user(user)
            db.session.commit()
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

        token = generate_confirmation_token(user.email)

        send_email_link(user.email,
                        f'{FlaskConfig.BACKEND_ADDRESS}/confirm_email?token={token}',
                        user.name)
        db.session.commit()
        return UserSchema(only=['id', 'name', 'email', 'role']).dump(user)


class ConfirmEmailResource(Resource):
    @staticmethod
    def get():
        try:
            token = request.args.get('token', None)

            if not token:
                return {'message': 'token required'}, 404

            email = confirm_token(token)

            if not email:
                return {"message": "Invalid token"}, 404

            user = User.query.filter_by(email=email).first()

            if user.confirmed_at:
                return {"message": "Not found"}, 404
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

            return redirect(FlaskConfig.FRONTEND_ADDRESS)

        except Exception as e:
            return {'message': "Internal server error", "error": e}


class LogoutResource(Resource):
    @staticmethod
    def post():
        try:
            user = User.query.get(current_user.id)
            user.remove_token()
            logout_user()
            return {"message": "success"}, 200
        except Exception as e:
            print(e)
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

        if not user or not user.is_active:
            return {'message': 'User not found'}, 404

        token = generate_confirmation_token(user.email)

        send_forgot_password_email(user.email,
                                   f'{FlaskConfig.FRONTEND_ADDRESS}/reset_password?token={token}',
                                   user.name)

        user.update({"reset_code": token, 'is_active': False})
        return {'message': 'success'}, 200


class CheckResetTokenResource(Resource):
    @staticmethod
    def post():
        data = request.json
        token = data.get('token', None)

        if not data or not token:
            return {'message': 'Reset code is required'}, 400

        email = confirm_token(token)

        if not email:
            return {"message": "Invalid token"}, 422

        user = User.query.filter_by(email=email).first()

        if not user or not user.reset_code or user.reset_code != token:
            return {"message": "Invalid token"}, 422

        return {'message': 'success'}, 200


class ResetPasswordResource(Resource):
    @staticmethod
    def post():
        try:
            data = request.json
            password = data.get('password', None)
            reset_code = data.get('token', None)

            if not reset_code:
                return {'message': 'Reset code is required'}, 400

            email = confirm_token(reset_code)

            if not email:
                return {"message": "Invalid token"}, 422

            user = User.query.filter_by(email=email).first()

            if not user or not user.reset_code or user.reset_code != reset_code:
                return {"message": "Invalid token"}, 422

            user.hash_password(password)
            user.update({"reset_code": None, "is_active": True})
            send_info_email(**{
                "subject": 'Аккаунт успешно востоновлен!',
                "message": "Ваш Аккаунт успешно востоновлен!",
                "recipient": user.email,
                "name": user.name
            })
            return {'message': 'success'}, 200
        except Exception as e:
            print(e)
            return {"message": "Internal Server Error"}, 500


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
        send_info_email(**{
            "subject": 'Изменение пароля!',
            "message": "Ваш пароль успешно изменен!",
            "recipient": user.email,
            "name": user.name
        })
        return {'message': 'success'}, 200


@login_manager.header_loader
def load_user_from_header(header_val):
    header_val = header_val.replace('Basic ', '', 1)
    try:
        if request.headers.get('Authorization', None):
            access_token = request.headers.get('Authorization').split(' ')[1]
            token = decode_token(access_token)
            token_expiry = datetime.fromtimestamp(token['exp'])

            if token_expiry < datetime.now():
                logout_user()
                return None

            user = User.query.get(token['identity'])

            if not user or not user.is_active or not user.token.access_token or user.token.access_token != access_token:
                return None

            return user

    except TypeError:
        pass

    return User.query.filter_by(api_key=header_val).first()


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)


app.session_interface = CustomSessionInterface()


@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
