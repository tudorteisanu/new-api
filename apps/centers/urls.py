from settings import app
from .views import get_centers_data
from .views import get_center_for_edit
from .views import create_center
from .views import edit_center
from .views import delete_center

resource = 'centers'

app.route(f'/{resource}', methods=['GET'])(get_centers_data)
app.route(f'/{resource}/<id>/edit', methods=['GET'])(get_center_for_edit)
app.route(f'/{resource}', methods=['POST'])(create_center)
app.route(f'/{resource}/<id>', methods=['PATCH'])(edit_center)
app.route(f'/{resource}', methods=['DELETE'])(delete_center)