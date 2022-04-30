from src.app import api
from .resource import ProfileResource
from .resource import ProfileOneResource

resource = '/profile'

api.add_resource(ProfileResource, resource)
api.add_resource(ProfileOneResource, f'{resource}/<user_id>')
