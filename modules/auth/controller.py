from config.settings import api
from modules.auth.service import LoginResource
from modules.auth.service import LogoutResource
from modules.auth.service import RegisterResource
from modules.auth.service import ForgotPasswordResource
from modules.auth.service import ResetPasswordResource
from modules.auth.service import ChangePasswordResource
from modules.auth.service import ConfirmEmailResource
from modules.auth.service import CheckResetTokenResource

api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(RegisterResource, '/register')
api.add_resource(ForgotPasswordResource, '/forgot_password')
api.add_resource(ResetPasswordResource, '/reset_password')
api.add_resource(ChangePasswordResource, '/change_password')
api.add_resource(ConfirmEmailResource, '/confirm_email')
api.add_resource(CheckResetTokenResource, '/check_reset_token')

import modules.auth.views