from flask_restful import Resource
from services.auth_utils import auth_required
from modules.users.service import UsersService


class UsersResource(Resource):
    def __init__(self):
        self.service = UsersService()

    @auth_required()
    def get(self):
        return self.service.find()

    @auth_required()
    def post(self):
        return self.service.create()


class UsersOneResource(Resource):
    def __init__(self):
        self.service = UsersService()

    @auth_required()
    def get(self, user_id):
        return self.service.find_one(user_id)

    @auth_required()
    def patch(self, user_id):
        return self.service.edit(user_id)

    @auth_required()
    def delete(self, user_id):
        return self.delete(user_id)


class UsersListResource(Resource):
    def __init__(self):
        self.service = UsersService()

    @auth_required()
    def get(self):
        return self.service.get_list()
   