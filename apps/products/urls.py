from settings import app
from .views import products_get_data
from .views import products_get_for_edit
from .views import products_create
from .views import products_edit
from .views import products_delete

app.route('/products', methods=['GET'])(products_get_data)
app.route('/products/<id>/edit', methods=['GET'])(products_get_for_edit)
app.route('/products', methods=['POST'])(products_create)
app.route('/products/<id>', methods=['PATCH'])(products_edit)
app.route('/products', methods=['DELETE'])(products_delete)
