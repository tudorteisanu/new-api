from settings import db, app, api
from views import get_data, get_for_edit, create, edit, delete


app.route('/users', methods=['GET'])(get_data)
app.route('/users/get_for_edit', methods=['GET'])(get_for_edit)
app.route('/users/create', methods=['PATCH'])(create)
app.route('/users/edit/<id>', methods=['GET'])(edit)
app.route('/users/delete/<id>', methods=['POST'])(delete)