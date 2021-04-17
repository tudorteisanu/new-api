from settings import app
from .views import  UserRoute as Route

resource = 'users'

app.route(f'/{resource}', methods=['GET'], endpoint=f'{resource}_index')(Route.get_data)
app.route(f'/{resource}/<id>/edit', methods=['GET'], endpoint=f'{resource}_get_for_edit')(Route.get_for_edit)
app.route(f'/{resource}', methods=['POST'], endpoint=f'{resource}_create')(Route.create)
app.route(f'/{resource}/<id>', methods=['PATCH'], endpoint=f'{resource}_edit')(Route.edit)
app.route(f'/{resource}/<id>', methods=['DELETE'], endpoint=f'{resource}_delete')(Route.delete)
