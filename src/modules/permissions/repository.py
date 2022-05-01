from src.app import db
from src.modules.permissions.models import Permission
from src.services.utils.repository import Repository


class PermissionRepository(Permission, Repository):
    @staticmethod
    def create(**kwargs):
        model = Permission(**kwargs)
        db.session.add(model)
        return model

    def paginate(self, page, per_page):
        return self.query \
            .paginate(page=page, per_page=per_page, error_out=False)

    def list(self):
        return [{"value": item.id, "text": item.alias} for item in self.query.all()]

    def get_by_ids(self, array):
        return self.query.filter(Permission.id.in_(array))

