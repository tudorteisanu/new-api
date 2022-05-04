import logging
from src.exceptions.permissions import PermissionsException
from .config.permissions import Permissions
from .service import NotificationService
from src.services.http import BaseResource
from src.services.http.auth_utils import auth_required
from src.services.http.response import InternalServerError


class NotificationResource(BaseResource):
    def __init__(self):
        self.service = NotificationService()
        self.permissions = Permissions.index

    @auth_required()
    def get(self):
        try:
            return self.service.find()
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
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class NotificationOneResource(BaseResource):
    def __init__(self):
        self.service = NotificationService()
        self.permissions = Permissions.self

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
        try:
            self.apply_permissions()
            return self.service.delete(model_id)
        except PermissionsException as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class NotificationListResource(BaseResource):
    def __init__(self):
        self.service = NotificationService()
        self.permissions = Permissions.list

    @auth_required()
    def get(self):
        try:
            return self.service.get_list()
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class NotificationCountResource(BaseResource):
    def __init__(self):
        self.service = NotificationService()

    @auth_required()
    def get(self):
        try:
            return self.service.get_count()
        except Exception as e:
            logging.error(e)
            return InternalServerError()
