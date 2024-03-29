# utf-8
import logging

from flask_restful import Resource

from src.exceptions.http import ValidationException, UnknownException
from src.modules.auth.service import AuthService
from src.services.http.auth_utils import auth_required
from src.services.http.response import InternalServerError
from src.services.http.response import UnprocessableEntity


class LoginResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def post(self):
        try:
            return self.service.login()
        except ValidationException as e:
            print(e.message)
            return UnprocessableEntity(errors=e.errors, message=e.message)
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class RegisterResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def post(self):
        try:
            return self.service.register()
        except ValidationException as e:
            return UnprocessableEntity(errors=e.errors)
        except UnknownException as e:
            logging.error(e)
            return InternalServerError()


class ConfirmEmailResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def get(self):
        return self.service.confirm_email()


class ReadUserResource(Resource):
    def __init__(self):
        self.service = AuthService()

    @auth_required()
    def get(self, model_id):
        return self.service.read(model_id)


class LogoutResource(Resource):
    def __init__(self):
        self.service = AuthService()

    @auth_required()
    def post(self):
        return self.service.logout()


class ForgotPasswordResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def post(self):
        return self.service.forgot_password()


class CheckResetTokenResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def post(self):
        return self.service.check_reset_token()


class CheckAuthResource(Resource):
    @auth_required()
    def get(self):
        return True


class ResetPasswordResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def post(self):
        return self.service.reset_password()


class ChangePasswordResource(Resource):
    def __init__(self):
        self.service = AuthService()

    @auth_required()
    def post(self):
        return self.service.change_password()
