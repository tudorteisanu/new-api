from src.app import api

from .resource import PermissionResource
from .resource import PermissionListResource
from .resource import PermissionOneResource

resource = '/permissions'

api.add_resource(PermissionResource, resource)
api.add_resource(PermissionOneResource, f'{resource}/<model_id>')
api.add_resource(PermissionListResource, f'{resource}/list')
