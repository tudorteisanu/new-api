from src.app import db


class Repository:
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
    def update(model, data):
        for (key, value) in data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        return model

    def paginate(self, **kwargs):
        query = self.query
        page = kwargs.get('page', 1)
        page_size = kwargs.get('page_size', 20)

        if kwargs.get('filters', None) is not None:
            for key in kwargs['filters']:
                if hasattr(self, key):
                    query = query.filter(getattr(self, key) == kwargs["filters"][key])

        response = query.paginate(page=page, per_page=page_size, error_out=False)

        return {
            "items": response.items,
            "pages": response.pages,
            "total": response.total,
            "page_size": page_size,
            "page": page,
        }

