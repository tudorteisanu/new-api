from settings import db, app, api
from .views import get_data, get_for_edit

#your routes here
app.route('/users', methods=['GET'])(get_data)
app.route('/users/edit/<id>', methods=['GET'])(get_for_edit)