from src.app import db
from src.modules.goods import Good
from flask import g
from src.services.utils import Pagination
from src.services.utils.repository import Repository


class GoodsRepository(Good, Repository):
    @staticmethod
    def create(**kwargs):
        model = Good(**kwargs)
        db.session.add(model)
        return model

    @staticmethod
    def paginate(**kwargs):
        pagination = Pagination(Good)
        return pagination(**kwargs)

    def list(self):
        return [{"value": item.id, "text": f'{getattr(self, f"name_{g.lang}")}'} for item in self.query.all()]

    def get_similar(self, model_id):
        return self.query.filter(self.id != model_id).all()
