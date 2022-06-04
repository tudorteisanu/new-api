from src.app import api
from src.modules.users.resource import UsersResource, UsersOneResource, UsersListResource

resource = '/users'

api.add_resource(UsersResource, resource)
api.add_resource(UsersOneResource, f'{resource}/<model_id>')
api.add_resource(UsersListResource, f'{resource}/list')
