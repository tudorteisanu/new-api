from flask_restful import Resource

from src.modules.roles.service import RoleService
from src.services.http.auth_utils import auth_required


class RolesResource(Resource):
    def __init__(self):
        self.service = RoleService()

    @auth_required()
    def get(self):
        return self.service.find()

    @auth_required()
    def post(self):
        return self.service.create()


class RolesOneResource(Resource):
    def __init__(self):
        self.service = RoleService()

    @auth_required()
    def get(self, model_id):
        return self.service.find_one(model_id)

    @auth_required()
    def patch(self, model_id):
        return self.service.edit(model_id)

    @auth_required()
    def delete(self, model_id):
        return self.service.delete(model_id)


class RolePermissionsResource(Resource):
    def __init__(self):
        self.service = RoleService()

    @auth_required()
    def get(self, model_id):
        return self.service.get_permissions(model_id)

    @auth_required()
    def put(self, model_id):
        return self.service.update_permissions(model_id)


class RolesListResource(Resource):
    def __init__(self):
        self.service = RoleService()

    @auth_required()
    def get(self):
        return self.service.get_list()
   