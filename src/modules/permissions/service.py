from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db

from src.modules.permissions.repository import PermissionRepository
from src.modules.permissions.serializer import CreatePermissionSerializer

from src.services.http.errors import Success
from src.services.http.errors import UnprocessableEntity
from src.services.http.errors import InternalServerError
from src.services.http.errors import NotFound


class PermissionService:
    def __init__(self):
        self.repository = PermissionRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "alias", "text": "Alias"}
        ]

        params = request.args

        page = int(params.get('page', 1))
        page_size = int(params.get('page_size', 20))

        items = self.repository.paginate(page, per_page=page_size)

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
            serializer = CreatePermissionSerializer(data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            self.repository.create(
                name=data['name'],
                alias=data['alias']
            )

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
                return NotFound(message='Permission not found')

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
