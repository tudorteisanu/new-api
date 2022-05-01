from src.app import db
from src.modules.users.models import User
from src.services.utils.repository import Repository


class UserRepository(User, Repository):
    @staticmethod
    def create(**kwargs):
        model = User(**kwargs)
        db.session.add(model)
        db.session.commit(model)
        return model

    def paginate(self, page, per_page, filters=None):
        query = self.query

        if filters is not None:
            if filters.get('email', None):
                query = query.filter(User.email.ilike(f'%{filters["email"]}%'))

            if filters.get('name', None):
                query = query.filter(User.name.ilike(f'%{filters["name"]}%'))

        return query \
            .paginate(page=page, per_page=per_page, error_out=False)

    def list(self):
        return [{"value": item.id, "text": item.name, "email": item.email} for item in self.query.all()]
