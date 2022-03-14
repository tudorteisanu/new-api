import logging
from json import loads

from flask import request, g
from flask_restful import Resource

from src.exceptions.permissions import PermissionsExceptions
from src.modules.roles.service import RoleService, RolePermissionsService
from src.services.http.auth_utils import auth_required
from src.services.http.errors import InternalServerError


class BaseResource(Resource):
    permissions = {}

    def apply_permissions(self):
        with open('config/permissions.json', 'r') as f:
            data = loads(f.read())
            if self.permissions.get(request.method, None) is None:
                raise PermissionsExceptions(message='Not have enough permissions')

            for item in self.permissions[request.method]:
                if item in data['admin']:
                    return True
            raise PermissionsExceptions(message='Not have enough permissions')


class RolesResource(BaseResource):
    permissions = {
        "GET": ["roles.index"],
        "POST": ["roles.store"]
    }

    @auth_required()
    def __init__(self):
        try:
            self.service = RoleService()
        except Exception as e:
            logging.error(e)

    def get(self):
        try:
            self.apply_permissions()
            return self.service.find()
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def post(self):
        return self.service.create()


class RolesOneResource(BaseResource):
    permissions = {
        "PATCH": []
    }

    @auth_required()
    def __init__(self):
        self.service = RoleService()

    def get(self, model_id):
        return self.service.find_one(model_id)

    def patch(self, model_id):
        try:
            self.apply_permissions()
            return self.service.edit(model_id)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def delete(self, model_id):
        return self.service.delete(model_id)


class RolePermissionsResource(BaseResource):
    @auth_required()
    def __init__(self):
        self.service = RolePermissionsService()

    def get(self, model_id):
        return self.service.get_permissions(model_id)

    def put(self, model_id):
        return self.service.update_permissions(model_id)


class RolesListResource(BaseResource):
    @auth_required()
    def __init__(self):
        self.service = RoleService()

    def get(self):
        return self.service.get_list()
   