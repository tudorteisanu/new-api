from flask import request, g
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db

from .repository import NotificationRepository
from .repository import UserReadNotificationRepository
from .serializer import CreateNotificationSerializer

from src.services.http.errors import Success
from src.services.http.errors import UnprocessableEntity
from src.services.http.errors import InternalServerError
from src.services.http.errors import NotFound


class NotificationService:
    def __init__(self):
        self.repository = NotificationRepository()
        self.user_notification_repository = UserReadNotificationRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "title", "text": 'Title'},
            {"value": "description", "text": 'Description'},
            {"value": "created_at", "text": 'Created at'},
        ]

        params = request.args
        page = int(params.get('page', 1))

        items = self.repository \
            .paginate(page=page, per_page=int(params.get('per_page', 20)))

        resp = {
            "items": [
                {
                    "id": item.id,
                    "title": item.title,
                    "description": item.description,
                    "created_at": item.created_at,
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "page": page,
            "headers": headers
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json or request.form
            serializer = CreateNotificationSerializer(data=data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            self.user_notification_repository.create(
                title=data['title'],
                description=data['description'],
            )
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
            params = request.args
            page = int(params.get('page', 1))

            items = self.repository \
                .paginate(page=page, per_page=int(params.get('per_page', 20)))

            resp = {
                "items": [
                    {
                        "id": item.id,
                        "title": item.title,
                        "description": item.description,
                        "created_at": item.created_at,
                        "read_at": self.set_read_at(item.id),
                    } for item in items.items],
                "pages": items.pages,
                "total": items.total,
                "page": page,
            }

            self.read_notifications(items.items)

            return jsonify(resp)

        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def get_count(self):
        try:
            notifications = self.repository.find()
            items = []
            for item in notifications:
                if not self.user_notification_repository.find_one(user_id=g.user.id, notification_id=item.id):
                    items.append(item)
            return len(items)
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def set_read_at(self, notification_id):
        notification = self.user_notification_repository.find_one(notification_id=notification_id, user_id=g.user.id)

        if notification:
            return notification.created_at

        return None

    def read_notifications(self, items):
        for item in items:
            notification = self.user_notification_repository.find_one(notification_id=item.id, user_id=g.user.id)

            if not notification:
                self.user_notification_repository.create(
                    notification_id=item.id,
                    user_id=g.user.id
                )

                db.session.commit()
