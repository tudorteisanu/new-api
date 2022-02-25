from application import api
from modules.users.resource import UsersResource
from modules.users.resource import UsersOneResource
from modules.users.resource import UsersListResource

resource = '/users'

api.add_resource(UsersResource, resource)
api.add_resource(UsersOneResource, f'{resource}/<model_id>')
api.add_resource(UsersListResource, f'{resource}/list')
