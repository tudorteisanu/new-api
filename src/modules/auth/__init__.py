from src.app import api
from .resource import LoginResource
from .resource import LogoutResource
from .resource import RegisterResource
from .resource import ResetPasswordResource
from .resource import ForgotPasswordResource
from .resource import ChangePasswordResource
from .resource import ConfirmEmailResource
from .resource import CheckResetTokenResource
from .resource import ReadUserResource

resource = '/auth'

api.add_resource(LoginResource, f'{resource}/login')
api.add_resource(LogoutResource, f'{resource}/logout')
api.add_resource(RegisterResource, f'{resource}/register')
api.add_resource(ForgotPasswordResource, f'{resource}/forgot_password')
api.add_resource(ResetPasswordResource, f'{resource}/reset_password')
api.add_resource(ChangePasswordResource, f'{resource}/change_password')
api.add_resource(ConfirmEmailResource, f'{resource}/activate')
api.add_resource(CheckResetTokenResource, f'{resource}/check_reset_token')
api.add_resource(ReadUserResource, '/users/<model_id>/read')
