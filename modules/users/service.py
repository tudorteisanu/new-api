import logging

from flask import request
from flask import jsonify
from flask_simple_serializer.response import Response

from modules.users.models import UserResource as User
from modules.users.schema import UserSchema
from services.auth_utils import auth_required
from flask_restful import Resource
from sqlalchemy import exc
from modules.users.serializer import CreateUserSerializer
from modules.users.repository import userRepository

from services.HttpErrors import InternalServerError
from services.HttpErrors import NotFoundError


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

        print(request.headers)

        serializer = CreateUserSerializer(data)

        if not serializer.is_valid():
            return Response(serializer.errors, status_code=422)

        try:
            user = User.create(data)
            return UserSchema(only=("name", "email", "role", 'id')).dump(user)
        except exc.IntegrityError:
            return {"message": 'User with same email exists.'}, 422


class UsersOneResource(Resource):
    @staticmethod
    @auth_required()
    def get(user_id):
        try:
            user = userRepository.find_one(user_id)
            return UserSchema().dump(user)
        except Exception as e:
            logging.log(e)
            return InternalServerError()

    @staticmethod
    @auth_required()
    def patch(user_id):
        data = request.json
        user = userRepository.find_one(user_id)
        if not user:
            return NotFoundError()

        user.update(data)
        return UserSchema(only=("name", "email", "role", 'id')).dump(user)

    @staticmethod
    @auth_required()
    def delete(user_id):
        user = userRepository.find_one(user_id)

        if not user:
            return {'message': "User not exists"}, 404
        user.delete()
        return {'message': 'Successful deleted'}, 200


class UsersListResource(Resource):
    @staticmethod
    @auth_required()
    def get():
        try:
            return userRepository.list()
        except Exception as e:
            logging.info(e)
            return InternalServerError()
