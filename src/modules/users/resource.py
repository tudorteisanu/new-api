import logging

from src.exceptions.permissions import PermissionsExceptions
from src.modules.users.service import UsersService
from src.services.http import BaseResource
from src.services.http.auth_utils import auth_required
from src.services.http.errors import InternalServerError
from src.modules.users.config.permissions import Permissions


class UsersResource(BaseResource):
    @auth_required()
    def __init__(self):
        self.service = UsersService()
        self.permissions = Permissions.index

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


class UsersOneResource(BaseResource):
    @auth_required()
    def __init__(self):
        self.service = UsersService()
        self.permissions = Permissions.self

    def get(self, model_id):
        try:
            self.apply_permissions()
            return self.service.find_one(model_id)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

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


class UsersListResource(BaseResource):
    @auth_required()
    def __init__(self):
        self.service = UsersService()
        self.permissions = Permissions.list

    def get(self):
        try:
            self.apply_permissions()
            return self.service.get_list()
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()
