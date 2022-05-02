from src.app import db
from .models import Category
from src.services.utils.repository import Repository


class CategoryRepository(Category, Repository):
    @staticmethod
    def create(**kwargs):
        model = Category(**kwargs)
        db.session.add(model)
        db.session.flush()
        return model

