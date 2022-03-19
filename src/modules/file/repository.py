from src.app import db
from .models import File


class FileRepository(File):
    @staticmethod
    def create(model):
        return db.session.add(model)

    @staticmethod
    def update(model, data):
        for (key, value) in data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        return model
