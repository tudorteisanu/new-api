from flask_restful import Resource

from src.modules.permissions.service import PermissionService
from src.services.http.auth_utils import auth_required


class PermissionResource(Resource):
    def __init__(self):
        self.service = PermissionService()

    @auth_required()
    def get(self):
        return self.service.find()

    @auth_required()
    def post(self):
        return self.service.create()


class PermissionOneResource(Resource):
    def __init__(self):
        self.service = PermissionService()

    @auth_required()
    def get(self, model_id):
        return self.service.find_one(model_id)

    @auth_required()
    def patch(self, model_id):
        return self.service.edit(model_id)

    @auth_required()
    def delete(self, model_id):
        return self.service.delete(model_id)


class PermissionListResource(Resource):
    def __init__(self):
        self.service = PermissionService()

    @auth_required()
    def get(self):
        return self.service.get_list()
   