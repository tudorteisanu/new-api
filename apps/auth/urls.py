from settings import app
from apps.auth.views import AuthRoute as Route

resource = 'auth'

app.route(f'/register', methods=['POST'], endpoint=f'{resource}_register')(Route.register)
app.route(f'/login', methods=['GET'], endpoint=f'{resource}_login')(Route.login)
app.route(f'/logout', methods=['GET'], endpoint=f'{resource}_logout')(Route.logout)
app.route(f'/check_token', methods=['GET'], endpoint=f'{resource}_check_token')(Route.check_token)
# app.route(f'/{resource}/<id>', methods=['DELETE'], endpoint=f'{resource}_delete')(Route.delete)
