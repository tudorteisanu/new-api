from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from src.modules.categories import Category
from src.modules.categories.repository import CategoryRepository
from src.modules.categories.serializer import CreateCategorySerializer

from src.services.http.errors import Success, UnprocessableEntity, InternalServerError, NotFound
from src.services.localization import Locales


class CategoriesService:
    def __init__(self):
        self.repository = CategoryRepository()
        self.t = Locales()

    def find(self):
        headers = ['id', "name_ro", "name_en", "name_ru", "author"]
        params = request.args
        items = self.repository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)))

        resp = {
            "items": [
                {
                    "id": item.id,
                    "name_ro": item.name_ro,
                    "name_en": item.name_en,
                    "name_ru": item.name_ru
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "headers": [{
                "value": item,
                "text": self.t.translate(f'categories.fields.{item}')
            } for item in headers]
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json
            serializer = CreateCategorySerializer(data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            model = Category(
                name_ro=data['name_ro'],
                name_en=data['name_en'],
                name_ru=data['name_ru']
            )
            self.repository.create(model)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def find_one(self, model_id):
        try:
            model = self.repository.find_one_or_fail(model_id)

            if not model:
                return NotFound(message=self.t.translate('categories.validation.not_found'))

            return {
                "name_ro": model.name_ro,
                "name_en": model.name_en,
                "name_ru": model.name_ru
            }
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def edit(self, user_id):
        try:
            data = request.json
            model = self.repository.get(user_id)

            if not model:
                return NotFound()

            self.repository.update(model, data)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            db.session.rollback()
            logging.error(e)
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def delete(self, model_id):
        try:
            model = self.repository.get(model_id)

            if not model:
                return NotFound()

            self.repository.remove(model)
            db.session.commit()
            return Success()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return InternalServerError()

    def get_list(self):
        try:
            return self.repository.list()
        except Exception as e:
            logging.error(e)
            return InternalServerError()
