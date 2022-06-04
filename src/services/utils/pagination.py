class Pagination:
    def __init__(self, model):
        self.model = model

    def __call__(self, **kwargs):
        query = self.model.query
        page = kwargs.get('page', 1)
        page_size = kwargs.get('page_size', 20)

        if kwargs.get('filters', None) is not None:
            for key in kwargs['filters']:
                if hasattr(self.model, key):
                    query = query.order_by(self.model.created_at).filter(getattr(self.model, key) == kwargs["filters"][key])

        response = query.paginate(page=page, per_page=page_size, error_out=False)

        return {
            "items": response.items,
            "pages": response.pages,
            "total": response.total,
            "page_size": page_size,
            "page": page,
        }
