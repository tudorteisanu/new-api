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

api.add_resource(LoginResource, '/auth/login')
api.add_resource(LogoutResource, '/auth/logout')
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(ForgotPasswordResource, '/auth/forgot_password')
api.add_resource(ResetPasswordResource, '/auth/reset_password')
api.add_resource(ChangePasswordResource, '/auth/change_password')
api.add_resource(ConfirmEmailResource, '/auth/activate')
api.add_resource(CheckResetTokenResource, '/auth/check_reset_token')
api.add_resource(ReadUserResource, '/users/<model_id>/read')

