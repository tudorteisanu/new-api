
from src.app import db
from .models import Notification


class NotificationRepository(Notification):
    def find(self, **kwargs):
        return self.query.filter_by(**kwargs).all()

    def get(self, model_id):
        return self.query.get(model_id)

    def find_one(self, **kwargs):
        return self.query.filter_by(**kwargs).first()

    def find_one_or_fail(self, model_id):
        return self.query.get(model_id)

    @staticmethod
    def remove(model):
        db.session.delete(model)
        return True

    @staticmethod
    def create(model):
        db.session.add(model)
        return True

    def paginate(self, page, per_page):
        return self.query \
            .paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def update(model, data):
        for (key, value) in data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        return model

    def list(self):
        return [{"value": item.id, "text": item.title} for item in self.query.all()]

