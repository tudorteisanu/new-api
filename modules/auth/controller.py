from api import api
from modules.auth.resource import LoginResource
from modules.auth.resource import LogoutResource
from modules.auth.resource import RegisterResource
from modules.auth.resource import ForgotPasswordResource
from modules.auth.resource import ResetPasswordResource
from modules.auth.resource import ChangePasswordResource
from modules.auth.resource import ConfirmEmailResource
from modules.auth.resource import CheckResetTokenResource
from modules.auth.resource import ReadUserResource

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

