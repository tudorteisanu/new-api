from config.settings import api
from modules.auth.service import LoginResource
from modules.auth.service import LogoutResource
from modules.auth.service import RegisterResource
from modules.auth.service import ForgotPasswordResource
from modules.auth.service import ResetPasswordResource

api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(RegisterResource, '/register')
api.add_resource(ForgotPasswordResource, '/forgot_password')
api.add_resource(ResetPasswordResource, '/reset_password')
