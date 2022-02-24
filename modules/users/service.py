from flask import request
from flask import jsonify
from flask_restful import Resource
from sqlalchemy import exc
import logging

from config.settings import db

from services.auth_utils import auth_required

from modules.users.models import User
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

        items = userRepository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)))

        resp = {
            "items": [
                {
                    "name": item.name,
                    "email": item.email,
                    "id": item.id,
                    "role": item.role
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }

        return jsonify(resp)

    @staticmethod
    @auth_required()
    def post():
        try:
            data = request.json or request.form
            user = User(
                name=data['name'],
                email=data['email']
            )
            userRepository.create(user)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()


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
        try:
            data = request.json
            user = userRepository.get(user_id)

            if not user:
                return NotFound()

            userRepository.update(user, data)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            logging.error(e)
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @staticmethod
    @auth_required()
    def delete(user_id):
        try:
            user = userRepository.get(user_id)

            if not user:
                return NotFound()

            userRepository.remove(user)
            db.session.commit()
            return Success()
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class UsersListResource(Resource):
    @staticmethod
    @auth_required()
    def get():
        try:
            return userRepository.list()
        except Exception as e:
            logging.error(e)
            return InternalServerError()
