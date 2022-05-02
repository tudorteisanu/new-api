
from src.app import db
from .models import Notification
from .models import UserReadNotification
from src.services.utils.repository import Repository


class NotificationRepository(Notification, Repository):
    @staticmethod
    def create(**kwargs):
        model = Notification(**kwargs)
        db.session.add(model)
        db.session.flush()
        return model

    def paginate(self, page, per_page):
        return self.query \
            .paginate(page=page, per_page=per_page, error_out=False)

    def list(self):
        return [{"value": item.id, "text": item.title} for item in self.query.all()]


class UserReadNotificationRepository(UserReadNotification, Repository):
    @staticmethod
    def create(**kwargs):
        model = UserReadNotification(**kwargs)
        db.session.add(model)
        db.session.flush()
        return model
