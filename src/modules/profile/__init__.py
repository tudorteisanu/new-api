from src.app import api
from .resource import ProfileResource

resource = '/profile'

api.add_resource(ProfileResource, resource)
