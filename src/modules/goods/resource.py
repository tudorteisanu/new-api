import logging

from src.exceptions.permissions import PermissionsException
from src.services.http import BaseResource
from src.services.http.auth_utils import auth_required
from src.services.http.response import InternalServerError

from .service import GoodsService


class GoodsResource(BaseResource):
    def __init__(self):
        self.service = GoodsService()

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
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class GoodsOneResource(BaseResource):
    def __init__(self):
        self.service = GoodsService()

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


class GoodsListResource(BaseResource):
    def __init__(self):
        self.service = GoodsService()

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


class GoodsPublicResource(BaseResource):
    def __init__(self):
        self.service = GoodsService()

    def get(self, category_id):
        try:
            return self.service.find_public(category_id)
        except PermissionsException as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class GoodsPublicListResource(BaseResource):
    def __init__(self):
        self.service = GoodsService()

    def get(self):
        try:
            return self.service.get_list()
        except PermissionsException as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class GoodsOnePublicListResource(BaseResource):
    def __init__(self):
        self.service = GoodsService()

    def get(self, model_id):
        try:
            return self.service.find_one_public(model_id)
        except PermissionsException as e:
            return {"message": e.message}, 403
        except Exception as e:
            logging.error(e)
            return InternalServerError()
