import logging

from flask import request
from flask import jsonify
from flask_restful import Resource
from sqlalchemy import exc

from services.auth_utils import auth_required

from modules.users.models import UserResource as User
from modules.users.schema import UserSchema
from modules.users.serializer import CreateUserSerializer
from modules.users.repository import userRepository

from services.HttpErrors import InternalServerError
from services.HttpErrors import NotFound
from services.HttpErrors import UnprocessableEntity
from services.HttpErrors import Success


class UsersResource(Resource):
    @staticmethod
    @auth_required()
    def get():
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "email", "text": "Email"},
            {"value": "role", "text": "Role"},
            {"value": "is_active", "text": "Active"}
        ]

        params = request.args

        items = User \
            .query \
            .paginate(page=int(params.get('page', 1)), per_page=int(params.get('per_page', 20)), error_out=False)

        resp = {
            "items": UserSchema(many=True).dump(items.items),
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }

        return jsonify(resp)

    @staticmethod
    @auth_required()
    def post():
        data = request.json or request.form
        serializer = CreateUserSerializer(data)

        if not serializer.is_valid():
            return UnprocessableEntity(errors=serializer.errors)
        try:
            user = User.create(data)
            return {
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "id": user.id
            }
        except exc.IntegrityError:
            return UnprocessableEntity(message="User with same email exists.")


class UsersOneResource(Resource):
    @staticmethod
    @auth_required()
    def get(user_id):
        try:
            user = userRepository.find_one_or_fail(user_id)
            
            if not user:
                return NotFound(message='User not found')

            return {
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "id": user.id
            }
        except Exception as e:
            print(e)
            return InternalServerError()

    @staticmethod
    @auth_required()
    def patch(user_id):
        data = request.json
        user = userRepository.find_one(user_id)
        if not user:
            return NotFound()

        user.update(data)
        return {
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "id": user.id
        }

    @staticmethod
    @auth_required()
    def delete(user_id):
        user = userRepository.find_one(user_id)

        if not user:
            return NotFound()
        user.delete()
        return Success()


class UsersListResource(Resource):
    @staticmethod
    @auth_required()
    def get():
        try:
            return userRepository.list()
        except Exception as e:
            logging.info(e)
            return InternalServerError()
