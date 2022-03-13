from src.app import api
from src.modules.roles.resource import RolesOneResource, RolesResource, RolesListResource, RolePermissionsResource

resource = '/roles'

api.add_resource(RolesResource, resource)
api.add_resource(RolesOneResource, f'{resource}/<model_id>')
api.add_resource(RolesListResource, f'{resource}/list')
api.add_resource(RolePermissionsResource, f'{resource}/<model_id>/permissions')
