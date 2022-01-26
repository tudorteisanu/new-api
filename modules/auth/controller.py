from config.settings import api
from modules.auth.service import LoginResource
from modules.auth.service import LogoutResource
from modules.auth.service import RegisterResource

api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(RegisterResource, '/register')
