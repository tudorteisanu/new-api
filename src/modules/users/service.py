from json import loads

from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging
from datetime import datetime as dt

from src.app import db
from src.modules.users.models import User
from src.modules.users.repository import UserRepository
from src.modules.roles.repository import RoleRepository

from src.services.http.errors import Success, UnprocessableEntity, InternalServerError, NotFound
from src.modules.users.serializer import CreateUserSerializer


class UsersService:
    def __init__(self):
        self.repository = UserRepository()
        self.role_repository = RoleRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "email", "text": "Email"},
            {"value": "roles", "text": "Roles"},
            {"value": "is_active", "text": "Active"}
        ]

        params = request.args
        page_size = int(params.get('page_size', 20))
        page = int(params.get('page', 1))
        filters = params.get('filters', None)

        if filters is not None:
            filters = loads(filters)

        items = self.repository.paginate(page, per_page=page_size, filters=filters)

        resp = {
            "items": [
                {
                    "name": item.name,
                    "email": item.email,
                    "id": item.id,
                    "roles": self.__get_string_user_roles(item.roles)
                } for item in items.items],
            "pages": items.pages,
            "page_size": page_size,
            "page": page,
            "total": items.total,
            "headers": headers
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json
            serializer = CreateUserSerializer(data)
            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            user = User()
            user.name = data['name'],
            user.email = data['email']
            user.confirmed_at = dt.utcnow().isoformat()
            user.is_active = True
            user.password = user.hash_password(data['password'])

            self.repository.create(user)
            if data.get('roles', None):
                self.repository.update(user, {"roles": data['roles']})
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
                "roles": [user_role.role_id for user_role in user.roles],
                "id": user.id
            }
        except Exception as e:
            logging.error(e)
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

    def __get_user_roles(self, roles):
        items = []

        for item in roles:
            role = self.role_repository.get(item.role_id)
            items.append({
                "name": role.name,
                "alias": role.alias,
                "id": role.id
            })

        return items

    def __get_string_user_roles(self, roles):
        items = self.__get_user_roles(roles)
        string_roles = []

        for item in items:
            string_roles.append(item['name'])

        return ", ".join(string_roles)
