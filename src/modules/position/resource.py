from flask_restful import Resource

from src.modules.position.service import PositionService
from src.services.http.auth_utils import auth_required


class PositionResource(Resource):
    def __init__(self):
        self.service = PositionService()

    @auth_required()
    def get(self):
        return self.service.find()

    @auth_required()
    def post(self):
        return self.service.create()


class PositionOneResource(Resource):
    def __init__(self):
        self.service = PositionService()

    @auth_required()
    def get(self, model_id):
        print(model_id)
        return self.service.find_one(model_id)

    @auth_required()
    def patch(self, model_id):
        return self.service.edit(model_id)

    @auth_required()
    def delete(self, model_id):
        return self.service.delete(model_id)


class PositionListResource(Resource):
    def __init__(self):
        self.service = PositionService()

    @auth_required()
    def get(self):
        return self.service.get_list()
   