from src.app import db
from src.modules.goods import Good
from flask import g


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

    def paginate(self, page, per_page, **kwargs):
        query = self.query

        if kwargs.get('filters', None) is not None:
            if kwargs['filters'].get('category_id', None):
                query = query.filter_by(category_id=kwargs['filters']['category_id'])

        return query \
            .paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def update(model, data):
        for (key, value) in data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        return model

    def list(self):
        return [{"value": item.id, "text": f'{getattr(self, f"name_{g.lang}")}'} for item in self.query.all()]
