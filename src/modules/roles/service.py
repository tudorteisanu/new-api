from json import loads

from flask import request, g
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from src.modules.roles.models import Role
from src.modules.roles.repository import RoleRepository, RolePermissionsRepository
from src.modules.roles.serializer import CreateRoleSerializer, PermissionsSerializer

from src.services.http.response import Success, UnprocessableEntity, InternalServerError, NotFound


class RoleService:
    def __init__(self):
        self.repository = RoleRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "alias", "text": "Alias"}
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
                    "alias": item.alias,
                    "id": item.id
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "page_size": page_size,
            "page": page,
            "headers": headers
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json
            serializer = CreateRoleSerializer(data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            user = Role(
                name=data['name'],
                alias=data['alias']
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
                return NotFound(message='Role not found')

            return {
                "name": user.name,
                "alias": user.alias,
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
            db.session.rollback()
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            logging.error(e)
            db.session.rollback()
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
            db.session.rollback()
            return InternalServerError()

    def get_list(self):
        try:
            return self.repository.list()
        except Exception as e:
            logging.error(e)
            return InternalServerError()


class RolePermissionsService:
    def __init__(self):
        self.repository = RolePermissionsRepository()

    def update_permissions(self, model_id):
        try:
            data = request.json
            serializer = PermissionsSerializer(data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            old_permissions = self.repository.find(role_id=model_id)

            for item in old_permissions:
                if not any(
                        item.endpoint == rule['endpoint']
                        and item.method == rule['method'] for rule in data['permissions']):
                    self.repository.remove(item)

            for item in data['permissions']:
                if not self.repository.find_one(endpoint=item['endpoint'], method=item['method'], role_id=model_id):
                    self.repository.create(
                        role_id=model_id,
                        endpoint=item['endpoint'],
                        method=item['method']
                    )

            db.session.commit()
            return Success()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return InternalServerError()

    def get_permissions(self, model_id):
        try:
            return [
                {"endpoint": item.endpoint, "method": item.method} for item in self.repository.find(role_id=model_id)
            ]
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def find_one(self, endpoint, method, role_id):
        try:
            user = self.repository.find_one(method=method, endpoint=endpoint, role_id=role_id)

            if not user:
                return None

            return {
                "id": user.id
            }
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @staticmethod
    def get_all_permissions():
        try:
            from src.app import app
            response = []
            for rule in app.url_map.iter_rules():
                for method in rule.methods:
                    if method not in ['HEAD', 'OPTIONS']:
                        response.append({"endpoint": rule.endpoint, "method": method})

            return response
        except Exception as e:
            logging.error(e)
            return InternalServerError()
