from settings import app
from .views import  AuthRoute


class Urls:
    register = '/register'
    login = '/login'
    logout = '/logout'
    check_token = '/check_token'
    user = '/users'
    logs = '/logs'


app.route(Urls.register, methods=["GET"])(AuthRoute.register)
app.route(Urls.login, methods=['GET'])(AuthRoute.login)
app.route(Urls.logout, methods=['GET'])(AuthRoute.logout)
app.route(Urls.check_token, methods=['GET'])(AuthRoute.check_token)
