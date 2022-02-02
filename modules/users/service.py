from flask import request
from flask import jsonify
from modules.users.models import User
from modules.users.schema import UserSchema
from services.auth_utils import auth_required
from flask_restful import Resource
from flask_simple_serializer.response import Response
from flask_simple_serializer.status_codes import HTTP_400_BAD_REQUEST
from sqlalchemy import exc
from modules.users.serializer import CreateUserSerializer


class UsersResource(Resource):
    @staticmethod
    @auth_required()
    def get():
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "email", "text": "Email"},
            {"value": "role", "text": "Role"}
        ]

        params = request.args

        items = User \
            .query \
            .order_by(User.id.desc()) \
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
        data = request.json
        serializer = CreateUserSerializer(data)

        if not serializer.is_valid():
            return Response(serializer.errors, status_code=HTTP_400_BAD_REQUEST)

        try:
            user = User(data)
            return UserSchema(only=("name", "email", "role", 'id')).dump(user)
        except exc.IntegrityError:
            return {"message": 'User with same email exists.'}, 422


class UsersOneResource(Resource):
    @staticmethod
    @auth_required()
    def get(user_id):
        user = User.query.get(user_id)
        return UserSchema().dump(user)

    @staticmethod
    @auth_required()
    def patch(user_id):
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return {'message': "User not found"}, 404

        user.update(data)
        return UserSchema(only=("name", "email", "role", 'id')).dump(user)

    @staticmethod
    @auth_required()
    def delete(user_id):
        user = User.query.get(user_id)

        if not user:
            return {'message': "User not exists"}, 404
        user.delete()
        return {'message': 'Successful deleted'}, 200


class UsersListResource(Resource):
    @staticmethod
    @auth_required()
    def get():
        users = User.query.all()
        return [{"value": user.id, "text": f'{user.name} - {user.email}'} for user in users]
