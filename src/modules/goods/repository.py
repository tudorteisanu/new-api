from src.app import db
from src.modules.goods import Good
from flask import g
from src.services.utils import Pagination


class GoodsRepository(Good):
    def find(self, **kwargs):
        return self.query.filter_by(**kwargs).all()

    def get(self, model_id):
        return self.query.get(model_id)

    def find_one(self, **kwargs):
        return self.query.filter_by(**kwargs).first()

    def find_one_or_fail(self, model_id):
        model = self.query.get(model_id)
        if model is None:
            raise Exception('Not found')
        return model

    @staticmethod
    def remove(model):
        db.session.delete(model)
        return True

    @staticmethod
    def create(model):
        db.session.add(model)
        return True

    @staticmethod
    def paginate(**kwargs):
        pagination = Pagination(Good)
        return pagination(**kwargs)

    @staticmethod
    def update(model, data):
        for (key, value) in data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        return model

    def list(self):
        return [{"value": item.id, "text": f'{getattr(self, f"name_{g.lang}")}'} for item in self.query.all()]
