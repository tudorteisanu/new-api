# utf-8
from flask_restful import Resource
from services.http.auth_utils import auth_required
from modules.auth.service import AuthService


class LoginResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def post(self):
        return self.service.login()


class RegisterResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def post(self):
        return self.service.register()


class ConfirmEmailResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def get(self):
        return self.service.confirm_email()


class ReadUserResource(Resource):
    def __init__(self):
        self.service = AuthService()

    def get(self, user_id):
        return self.service.read(user_id)


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
