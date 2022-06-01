import logging

from src.exceptions.http import ValidationException
from src.exceptions.permissions import PermissionsException
from src.modules.users.service import UsersService
from src.services.http import BaseResource
from src.services.http.auth_utils import auth_required
from src.services.http.response import InternalServerError
from src.services.http.response import UnprocessableEntity


class UsersResource(BaseResource):
    def __init__(self):
        self.service = UsersService()

    @auth_required()
    def get(self):
        try:
            self.apply_permissions()
            return self.service.find()
        except PermissionsException as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @auth_required()
    def post(self):
        try:
            self.apply_permissions()
            return self.service.create()
        except PermissionsException as e:
            return {"message": e.message}, 403
        except ValidationException as e:
            print(UnprocessableEntity(message=e.message, errors=e.errors), '-----resource-')
            return UnprocessableEntity(message=e.message, errors=e.errors)
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class UsersOneResource(BaseResource):
    def __init__(self):
        self.service = UsersService()

    @auth_required()
    def get(self, model_id):
        try:
            self.apply_permissions()
            return self.service.find_one(model_id)
        except PermissionsException as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @auth_required()
    def patch(self, model_id):
        try:
            self.apply_permissions()
            return self.service.edit(model_id)
        except PermissionsException as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @auth_required()
    def delete(self, model_id):
        return self.service.delete(model_id)


class UsersListResource(BaseResource):
    def __init__(self):
        self.service = UsersService()

    @auth_required()
    def get(self):
        try:
            self.apply_permissions()
            return self.service.get_list()
        except PermissionsException as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()
