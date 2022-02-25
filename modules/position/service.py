from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from api import db

from modules.position.models import Position
from modules.position.repository import PositionRepository

from services.http.errors import InternalServerError
from services.http.errors import NotFound
from services.http.errors import UnprocessableEntity
from services.http.errors import Success


class PositionService:
    def __init__(self):
        self.repository = PositionRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name_ro", "text": 'Name RO'},
            {"value": "name_en", "text": 'Name EN'},
            {"value": "name_ru", "text": 'Name RU'},
        ]

        params = request.args

        items = self.repository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)))

        resp = {
            "items": [
                {
                    "name_ro": item.name_ro,
                    "name_en": item.name_en,
                    "name_ru": item.name_ru,
                    "id": item.id,
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json or request.form
            user = Position(
                name_ro=data['name_ro'],
                name_en=data['name_en'],
                name_ru=data['name_ru']
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
                return NotFound(message='Position not found')

            return {
                "name_ro": user.name_ro,
                "name_en": user.name_en,
                "name_ru": user.name_ru,
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

    def delete(self, model_id):
        try:
            model = self.repository.get(model_id)

            if not model:
                return NotFound()

            self.repository.remove(model)
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
