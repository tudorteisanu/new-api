from flask import request, g
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from src.exceptions.http import UnknownException, ValidationException
from src.modules.categories.repository import CategoryRepository
from src.modules.categories.serializer import CreateCategorySerializer

from src.services.http.response import Success
from src.services.http.response import UnprocessableEntity
from src.services.http.response import InternalServerError
from src.services.http.response import NotFound

from src.services.localization import Locales
from src.modules.file import file_service


class CategoriesService:
    def __init__(self):
        self.repository = CategoryRepository()
        self.file_service = file_service
        self.t = Locales()

    def find(self):
        headers = ['id', "name_ro", "name_en", "name_ru", "image", "author"]
        params = request.args
        items = self.repository \
            .paginate(page=int(params.get('page', 1)), per_page=int(params.get('per_page', 20)))
        print(items['items'], 'items')
        resp = {
            **items,
            "items": [
                {
                    "id": item.id,
                    "name_ro": item.name_ro,
                    "name_en": item.name_en,
                    "name_ru": item.name_ru,
                    "image": {
                        "url": item.image.get_url() if item.image else '',
                        "name": item.image.name if item.image else ''
                    }
                } for item in items['items']],
            "headers": [{
                "value": item,
                "text": self.t.translate(f'categories.fields.{item}')
            } for item in headers]
        }
        return resp

    def create(self):
        try:
            data = request.form
            serializer = CreateCategorySerializer(data)

            if not serializer.is_valid():
                raise ValidationException(errors=serializer.errors)

            file = request.files.get('image', None)

            self.repository.create(
                name_ro=data['name_ro'],
                name_en=data['name_en'],
                name_ru=data['name_ru'],
                file_id=self.file_service.save_file(file, 'categories') or None
            )

            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            raise ValidationException(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            raise UnknownException()

    def find_one(self, model_id):
        try:
            model = self.repository.find_one_or_fail(model_id)

            if not model:
                return NotFound(message=self.t.translate('categories.validation.not_found'))

            response = {
                "name_ro": model.name_ro,
                "name_en": model.name_en,
                "name_ru": model.name_ru,
                "image": {
                    "url": model.image.get_url() if model.image else '',
                    "name": model.image.name if model.image else ''
                }
            }

            if model.image:
                response['image'] = model.image.dict()

            return response
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def edit(self, user_id):
        try:
            data = request.form
            model = self.repository.get(user_id)

            if not model:
                return NotFound()

            file = request.files.get('image', None)

            if file:
                model.file_id = self.file_service.save_file(file, 'categories') or None

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
            items = self.repository.list()
            return [{"value": item.id, "text": f'{getattr(item, f"name_{g.language}")}'} for item in items]
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def get_public_list(self):
        try:
            items = self.repository.list()
            return [
                {
                    "value": item.id,
                    "text": f'{getattr(item, f"name_{g.language}")}',
                    "image_url": item.image.get_url() if item.image else ""
                } for item in items]
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def public(self):
        headers = ['id', "name_ro", "name_en", "name_ru", "author"]
        params = request.args
        page = int(params.get('page', 1))
        page_size = int(params.get('page_size', 20))
        items = self.repository \
            .paginate(page=page, per_page=page_size)

        resp = {
            "items": [
                {
                    "id": item.id,
                    "name": getattr(item, f'name_{g.language}'),
                    "url": item.image.get_url() if item.image else ""
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "page_size": page_size,
            "page": page,
            "headers": [{
                "value": item,
                "text": self.t.translate(f'categories.fields.{item}')
            } for item in headers]
        }

        return jsonify(resp)
