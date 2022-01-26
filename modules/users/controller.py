from config.settings import api
from modules.users.service import UsersResource
from modules.users.service import UsersOneResource
from modules.users.service import UsersListResource

resource = '/users'

api.add_resource(UsersResource, resource)
api.add_resource(UsersOneResource, f'{resource}/<user_id>')
api.add_resource(UsersListResource, f'{resource}/list')
