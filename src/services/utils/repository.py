from src.app import db


class Repository:
    def find(self, **kwargs):
        try:
            return self.query.filter_by(**kwargs).all()
        except Exception as e:
            raise e

    def get(self, model_id):
        return self.query.get(model_id)

    def find_one(self, **kwargs):
        try:
            return self.query.filter_by(**kwargs).first()
        except Exception as e:
            raise e

    def find_one_or_fail(self, model_id):
        try:
            return self.query.get(model_id)
        except Exception as e:
            raise e

    @staticmethod
    def remove(model):
        try:
            db.session.delete(model)
            return True
        except Exception as e:
            raise e

    @staticmethod
    def update(model, data):
        try:
            for (key, value) in data.items():
                if hasattr(model, key):
                    setattr(model, key, value)
            return model
        except Exception as e:
            raise e

    def paginate(self, **kwargs):
        try:
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
        except Exception as e:
            raise e
