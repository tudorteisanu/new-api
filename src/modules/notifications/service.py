from flask import request, g
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from .models import Notification, UserReadNotification
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

    @staticmethod
    def get_count():
        try:
            notifications = Notification.query.all()
            items = []
            for item in notifications:
                if not UserReadNotification.query.filter_by(user_id=g.user.id, notification_id=item.id).first():
                    items.append(item)
            return len(items)
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    @staticmethod
    def set_read_at(notification_id):
        notification = UserReadNotification.query.filter_by(notification_id=notification_id, user_id=g.user.id).first()

        if notification:
            return notification.created_at

        return None

    @staticmethod
    def read_notifications(items):
        for item in items:
            notification = UserReadNotification.query.filter_by(notification_id=item.id, user_id=g.user.id).first()

            if not notification:
                new_read_notification = UserReadNotification()
                new_read_notification.notification_id = item.id
                new_read_notification.user_id = g.user.id
                db.session.add(new_read_notification)
                db.session.commit()

