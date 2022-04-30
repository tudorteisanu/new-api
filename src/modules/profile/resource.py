import logging
from src.exceptions.permissions import PermissionsExceptions
from .config.permissions import Permissions
from .service import ProfileService
from src.services.http import BaseResource
from src.services.http.auth_utils import auth_required
from src.services.http.errors import InternalServerError


class ProfileResource(BaseResource):
    def __init__(self):
        self.service = ProfileService()
        self.permissions = Permissions.self

    @auth_required()
    def get(self):
        try:
            self.apply_permissions()
            return self.service.show()
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @auth_required()
    def put(self):
        try:
            self.apply_permissions()
            return self.service.update()
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class ProfileOneResource(BaseResource):
    def __init__(self):
        self.service = ProfileService()
        self.permissions = Permissions.self

    @auth_required()
    def get(self, user_id):
        try:
            self.apply_permissions()
            return self.service.show(user_id)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @auth_required()
    def put(self, user_id):
        try:
            self.apply_permissions()
            return self.service.update(user_id)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()
