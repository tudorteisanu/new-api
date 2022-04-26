from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from .models import Notification
from .repository import NotificationRepository
from .serializer import CreateNotificationSerializer
from src.services.http.errors import Success, UnprocessableEntity, InternalServerError, NotFound


class NotificationService:
    def __init__(self):
        self.repository = NotificationRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "title", "text": 'Title'},
            {"value": "description", "text": 'Description'},
        ]

        params = request.args

        items = self.repository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)))

        resp = {
            "items": [
                {
                    "id": item.id,
                    "title": item.title,
                    "description": item.description,

                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json or request.form

            serializer = CreateNotificationSerializer(data=data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            model = Notification(
                title=data['title'],
                description=data['description'],

            )
            self.repository.create(model)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def find_one(self, model_id):
        try:
            model = self.repository.find_one_or_fail(model_id)

            if not model:
                return NotFound(message='Notification not found')

            return {
                    "id": model.id,
                    "title": model.title,
                    "description": model.description,
                }
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def edit(self, user_id):
        try:
            data = request.json
            model = self.repository.get(user_id)

            if not model:
                return NotFound()

            self.repository.update(model, data)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            db.session.rollback()
            logging.error(e)
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
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
            db.session.rollback()
            return InternalServerError()

    def get_list(self):
        try:
            return self.repository.list()
        except Exception as e:
            logging.error(e)
            return InternalServerError()
