from src.app import api
from src.modules.roles.resource import RolesOneResource
from src.modules.roles.resource import RolesResource
from src.modules.roles.resource import RolesListResource
from src.modules.roles.resource import RolePermissionsResource
from src.modules.roles.resource import RolesPermissionsListResource

resource = '/roles'

api.add_resource(RolesResource, resource)
api.add_resource(RolesOneResource, f'{resource}/<model_id>')
api.add_resource(RolesListResource, f'{resource}/list')
api.add_resource(RolePermissionsResource, f'{resource}/<model_id>/permissions')
api.add_resource(RolesPermissionsListResource, f'{resource}/permissions/list')
