from src.app import db
from .models import Category
from src.services.utils.repository import Repository


class CategoryRepository(Category, Repository):
    @staticmethod
    def create(**kwargs):
        try:
            model = Category(**kwargs)
            db.session.add(model)
            db.session.flush()
            return model
        except Exception as e:
            print(e)
            raise e

    def list(self):
        return [
            {
                "value": item.id,
                "text": item.name_ro
            } for item in self.query.with_entities(Category.id, Category.name_ro).all()
        ]

