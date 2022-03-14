from src.app import db
from src.modules.users.models import User, UserRole


class UserRepository(User):
    def find(self, **kwargs):
        return self.query.filter_by(**kwargs).all()

    def get(self, user_id):
        return self.query.get(user_id)

    def find_one(self, **kwargs):
        return self.query.filter_by(**kwargs).first()

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
                if key != 'roles':
                    setattr(model, key, value)
                else:
                    for item in model.roles:
                        if item.role_id not in data[key]:
                            db.session.delete(item)

                    for item in data[key]:
                        user_role = UserRole.query.filter_by(user_id=model.id, role_id=item).first()

                        if user_role is None:
                            db.session.add(UserRole(user_id=model.id, role_id=item))


        return model

    def list(self):
        return [{"value": item.id, "text": item.name, "email": item.email} for item in self.query.all()]

