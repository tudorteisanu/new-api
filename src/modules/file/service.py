import hashlib
import logging
import os
from random import random
from werkzeug.utils import secure_filename
from src.app.config import FlaskConfig

from src.app import app
from src.app import db
from src.services.localization import Locales

from .repository import FileRepository


class FileService:
    def __init__(self):
        self.t = Locales()
        self.repository = FileRepository()

    def save_file(self, file, module='images'):
        try:
            if not file:
                raise "File is required"

            filename = f'{hashlib.md5(secure_filename(file.filename).encode()).hexdigest()}{random()}.{file.filename.split(".")[1]}'
            current_path = os.path.dirname(app.instance_path)
            relative_file_path = f'static/{module}/{filename}'
            file_path = f'{current_path}/{relative_file_path}'
            file.save(file_path)
            file_object = self.repository.create(
                size=os.stat(file_path).st_size,
                mime_type=file.mimetype,
                path=f'{relative_file_path}',
                name=file.filename
            )

            db.session.flush()
            return file_object.id
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return None

    def save_file_from_object(self, filename, file_path):
        try:
            current_path = os.path.dirname(app.instance_path)

            file_object = self.repository.create(
                size=os.stat(f'{current_path}/{file_path}').st_size,
                mime_type='image/jpeg',
                path=f'{file_path}',
                name=filename
            )

            db.session.flush()
            return file_object.id
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return None

    @staticmethod
    def get_file_url(file):
        if file is None:
            return ""

        return f'{FlaskConfig.STATIC_PATH}/{file.path}'
