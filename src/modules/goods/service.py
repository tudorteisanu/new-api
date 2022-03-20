from json import loads

from flask import request, g
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from src.modules.goods import Good
from src.modules.goods.repository import GoodsRepository
from src.modules.goods.serializer import CreateGoodSerializer

from src.services.http.errors import Success, UnprocessableEntity, InternalServerError, NotFound
from src.services.localization import Locales
from src.modules.file import file_service


class GoodsService:
    def __init__(self):
        self.repository = GoodsRepository()
        self.t = Locales()

    def find(self):
        headers = ['id', "name_ro", "name_en", "name_ru", "category", "author"]
        params = request.args
        filters = params.get('filters', None)

        if filters is not None:
            print(filters)
            filters = loads(filters)

        items = self.repository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)), filters=filters)

        resp = {
            "items": [
                {
                    "id": item.id,
                    "name_ro": item.name_ro,
                    "name_en": item.name_en,
                    "name_ru": item.name_ru,
                    "url": item.image.get_url() if item.image else '',
                    "category_id": item.category_id
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "headers": [{
                "value": item,
                "text": self.t.translate(f'goods.fields.{item}')
            } for item in headers]
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.form
            serializer = CreateGoodSerializer(data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            model = Good(
                name_ro=data['name_ro'],
                name_en=data['name_en'],
                name_ru=data['name_ru'],
                category_id=data.get('category_id', None),
                description_en=data.get('description_en', None),
                description_ro=data.get('description_ro', None),
                description_ru=data.get('description_ru', None),
                height=data.get('height', None),
                width=data.get('width', None),
                length=data.get('length', None),
                price=data.get('price', None),
            )

            file = request.files.get('image', None)

            if file:
                model.file_id = file_service.save_file(file, 'goods') or None

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
                return NotFound(message=self.t.translate('goods.validation.not_found'))

            return {
                "name_ro": model.name_ro,
                "name_en": model.name_en,
                "name_ru": model.name_ru,
                "width": model.width,
                "height": model.height,
                "length": model.length,
                "price": model.price,
                "description_en": model.description_en,
                "description_ro": model.description_ro,
                "description_ru": model.description_ru,
                "category_id": model.category_id,
                "image": {
                    "url": model.image.get_url() if model.image else '',
                    "name": model.image.name if model.image else ''
                }
            }
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
                model.file_id = file_service.save_file(file, 'goods') or None

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

    def find_public(self, category_id):
        params = request.args
        # filters = params.get('filters', None)
        #
        # if filters is not None:
        #     filters = loads(filters)

        filters = {
            "category_id": category_id
        }

        items = self.repository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)), filters=filters)

        resp = {
            "items": [
                {
                    "id": item.id,
                    "name": getattr(item, f'name_{g.language}'),
                    "description": getattr(item, f'description_{g.language}'),
                    "width": item.width,
                    "height": item.height,
                    "length": item.length,
                    "price": item.price,
                    "image_url": item.image.get_url() if item.image else '',
                    "category_id": item.category_id
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
        }

        return jsonify(resp)

    def find_one_public(self, model_id):
        try:
            model = self.repository.find_one_or_fail(model_id)

            if not model:
                return NotFound(message=self.t.translate('goods.validation.not_found'))

            response = {
                "name": getattr(model, f'name_{g.language}'),
                "width": model.width,
                "height": model.height,
                "length": model.length,
                "price": model.price,
                "description": getattr(model, f'description_{g.language}'),
                "image_url": model.image.get_url() if model.image else ''
            }

            if model.category:
                response['category'] = {
                    'id': model.category.id,
                    'name': getattr(model.category, f'name_{g.language}'),
                }
            return response
        except Exception as e:
            logging.error(e)
            return InternalServerError()
