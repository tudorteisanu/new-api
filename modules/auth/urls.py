from config.settings import app
from modules.auth.views import AuthRoute as Route

resource = 'auth'

app.route(f'/register', methods=['GET'], endpoint=f'{resource}_register')(Route.register)
app.route(f'/login', methods=['GET'], endpoint=f'{resource}_login')(Route.login)
app.route(f'/logout', methods=['GET'], endpoint=f'{resource}_logout')(Route.logout)
app.route(f'/check_token', methods=['GET'], endpoint=f'{resource}_check_token')(Route.check_token)
app.route(f'/reset_password_step_1', methods=['GET'], endpoint=f'{resource}_reset_step_1')(Route.reset_password_step_1)
