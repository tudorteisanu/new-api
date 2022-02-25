from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from api import db

from modules.users.models import User
from modules.users.repository import UserRepository

from services.http.errors import InternalServerError
from services.http.errors import NotFound
from services.http.errors import UnprocessableEntity
from services.http.errors import Success


class UsersService:
    def __init__(self):
        self.repository = UserRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "email", "text": "Email"},
            {"value": "role", "text": "Role"},
            {"value": "is_active", "text": "Active"}
        ]

        params = request.args

        items = self.repository \
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

    def create(self):
        try:
            data = request.json or request.form
            user = User(
                name=data['name'],
                email=data['email']
            )
            self.repository.create(user)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def find_one(self, user_id):
        try:
            user = self.repository.find_one_or_fail(user_id)

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

    def edit(self, user_id):
        try:
            data = request.json
            user = self.repository.get(user_id)

            if not user:
                return NotFound()

            self.repository.update(user, data)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            logging.error(e)
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def delete(self, user_id):
        try:
            user = self.repository.get(user_id)

            if not user:
                return NotFound()

            self.repository.remove(user)
            db.session.commit()
            return Success()
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def get_list(self):
        try:
            return self.repository.list()
        except Exception as e:
            logging.error(e)
            return InternalServerError()
