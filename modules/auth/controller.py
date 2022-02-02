from config.settings import api
from modules.auth.service import LoginResource
from modules.auth.service import LogoutResource
from modules.auth.service import RegisterResource
from modules.auth.service import ForgotPasswordResource
from modules.auth.service import ResetPasswordResource
from modules.auth.service import ChangePasswordResource
from modules.auth.service import ConfirmEmailResource
from modules.auth.service import CheckResetTokenResource

api.add_resource(LoginResource, '/auth/login')
api.add_resource(LogoutResource, '/auth/logout')
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(ForgotPasswordResource, '/auth/forgot_password')
api.add_resource(ResetPasswordResource, '/auth/reset_password')
api.add_resource(ChangePasswordResource, '/auth/change_password')
api.add_resource(ConfirmEmailResource, '/auth/confirm_email')
api.add_resource(CheckResetTokenResource, '/auth/check_reset_token')

import modules.auth.views