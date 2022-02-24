from modules.users.models import User
from config.settings import db
import logging


class UserRepository(User):
    def find(self):
        return self.query.all()

    def find_one(self, user_id):
        return self.query.get(user_id)

    def find_one_or_fail(self, user_id):
        return self.query.get(user_id)

    @staticmethod
    def remove(user):
        db.session.delete(user)
        return True

    @staticmethod
    def create(user):
        db.session.add(user)
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
        return [{"value": item.id, "text": item.name, "email": item.email} for item in self.query.all()]


userRepository = UserRepository()
