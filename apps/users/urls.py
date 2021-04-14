from settings import app
from .views import get_user_data
from .views import get_user_for_edit
from .views import  create_user
from .views import  edit_user
from .views import  delete_user

resource = 'users'

app.route(f'/{resource}', methods=['GET'])(get_user_data)
app.route(f'/{resource}/<id>/edit', methods=['GET'])(get_user_for_edit)
app.route(f'/{resource}', methods=['POST'])(create_user)
app.route(f'/{resource}/<id>', methods=['PATCH'])(edit_user)
app.route(f'/{resource}', methods=['DELETE'])(delete_user)