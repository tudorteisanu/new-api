from src.app import db
from .models import File


class FileRepository(File):
    @staticmethod
    def create(**kwargs):
        model = File(**kwargs)
        db.session.add(model)
        return model

    @staticmethod
    def update(model, data):
        for (key, value) in data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        return model
