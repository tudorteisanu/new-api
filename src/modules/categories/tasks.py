from threading import Thread

from src.app import db, app
import time
from .service import CategoryRepository
from ..file import file_service

repository = CategoryRepository()


def save(data, file):
    my_thread = Thread(target=create_category, kwargs={**data, "file": file})
    my_thread.start()


def create_category(**kwargs):
    try:
        file = kwargs.get('file', None)
        with app.app_context():
            repository.create(
                name_ro=kwargs['name_ro'],
                name_en=kwargs['name_en'],
                name_ru=kwargs['name_ru'],
                file_id=file_service.save_file(file, 'categories') or None
            )

            time.sleep(10)
            db.session.commit()
            return True
    except Exception as e:
        db.session.rollback()
        raise e
