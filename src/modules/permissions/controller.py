from src.app import api
from src.modules.permissions.resource import PermissionResource, PermissionListResource, PermissionOneResource

resource = '/permissions'

api.add_resource(PermissionResource, resource)
api.add_resource(PermissionOneResource, f'{resource}/<model_id>')
api.add_resource(PermissionListResource, f'{resource}/list')
