import logging
from src.exceptions.permissions import PermissionsExceptions
from .config.permissions import Permissions
from .service import ProfileService
from src.services.http import BaseResource
from src.services.http.auth_utils import auth_required
from src.services.http.response import InternalServerError
from src.services.http.response import UnprocessableEntity
from src.services.http.response import NotFound
from flask import request

from src.exceptions.http import UnknownError
from src.exceptions.http import NotFoundException
from src.exceptions.http import ValidationError


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
        except UnknownError as e:
            logging.error(e)
            return InternalServerError()
        except NotFoundException as e:
            return NotFound(message=e.message)

    @auth_required()
    def put(self):
        try:
            self.apply_permissions()
            return self.service.update(request.json)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except ValidationError as e:
            return UnprocessableEntity(errors=e.errors)
        except UnknownError as e:
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
        except UnknownError as e:
            logging.error(e)
            return InternalServerError()
        except NotFoundException as e:
            return NotFound(message=e.message)

    @auth_required()
    def put(self, user_id):
        try:
            self.apply_permissions()
            return self.service.update(user_id, request.json)
        except PermissionsExceptions as e:
            return {"message": e.message}, 403
        except ValidationError as e:
            return UnprocessableEntity(errors=e.errors)
        except UnknownError as e:
            logging.error(e)
            return InternalServerError()
