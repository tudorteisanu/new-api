from json import loads

from flask import request, g
from flask import jsonify
from sqlalchemy import exc
import logging

from src.app import db
from src.modules.goods.repository import GoodsRepository
from src.modules.goods.repository import GoodsFileRepository
from src.modules.goods.serializer import CreateGoodSerializer

from src.services.http.response import Success
from src.services.http.response import UnprocessableEntity
from src.services.http.response import InternalServerError
from src.services.http.response import NotFound
from src.services.localization import Locales
from src.modules.file import file_service
from random import sample


class GoodsService:
    def __init__(self):
        self.repository = GoodsRepository()
        self.t = Locales()
        self.goods_files_repository = GoodsFileRepository()
        self.file_service = file_service

    def find(self):
        headers = ['id', "name_ro", "name_en", "name_ru", "category", "author"]
        params = request.args
        filters = params.get('filters', None)

        page = int(params.get('page', 1))
        page_size = int(params.get('page_size', 20))

        if filters is not None:
            filters = loads(filters)

        response = self.repository.paginate(page=page, page_size=page_size, filters=filters)

        resp = {
            **response,
            "items": [
                {
                    "id": item.id,
                    "name_ro": item.name_ro,
                    "name_en": item.name_en,
                    "name_ru": item.name_ru,
                    "url": self.get_first_image(item),
                    "category_id": item.category_id
                } for item in response['items']],
            "headers": [{
                "value": item,
                "text": self.t.translate(f'goods.fields.{item}')
            } for item in headers]
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.form
            serializer = CreateGoodSerializer(data=data)

            if not serializer.is_valid():
                return UnprocessableEntity(errors=serializer.errors)

            good = self.repository.create(
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

            files = request.files

            if len(files):
                for file in files:
                    file_id = self.file_service.save_file(files[file], 'categories') or None
                    self.goods_files_repository.create(file_id=file_id, category_id=good.id)

            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            print(e)
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
                "images": self.get_images(model.images)
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

            files = request.files

            self.check_files(model.images, self.parse_images(data))

            if len(files):
                for file in files:
                    file_id = self.file_service.save_file(files[file], 'goods') or None
                    self.goods_files_repository.create(file_id=file_id, good_id=model.id)

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

        filters = {
            "category_id": category_id
        }

        page = int(params.get('page', 1))
        page_size = int(params.get('page_size', 20))
        response = self.repository.paginate(page=page, page_size=page_size, filters=filters)

        resp = {
            **response,
            "items": [
                {
                    "id": item.id,
                    "name": getattr(item, f'name_{g.language}'),
                    "width": item.width,
                    "height": item.height,
                    "length": item.length,
                    "price": item.price,
                    "images": self.get_images(item.images),
                    "category_id": item.category_id
                } for item in response['items']],
        }

        return jsonify(resp)

    def find_one_public(self, model_id):
        try:
            model = self.repository.find_one_or_fail(model_id)

            if not model:
                return NotFound(message=self.t.translate('goods.validation.not_found'))

            random_goods = self.get_similar_products(model)

            response = {
                "id": model.id,
                "name": getattr(model, f'name_{g.language}'),
                "width": model.width,
                "height": model.height,
                "length": model.length,
                "price": model.price,
                "description": getattr(model, f'description_{g.language}'),
                "images": self.get_images(model.images),
                # "items": [{
                #     "id": item.id,
                #     "name": getattr(item, f'name_{g.language}'),
                #     "image_url": item.image.get_url() if item.image else '',
                #     "price": item.price
                # } for item in random_goods]
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

    def get_similar_products(self, model, count=5):
        items = self.repository.get_similar(model.id)
        if len(items) > count:
            return sample(items, count)
        return items

    @staticmethod
    def get_first_image(item):
        if len(item.images) > 0:
            return item.images[0].file.get_url() or None

        return None

    def get_images(self, images):
        files = []

        for item in images:
            file = self.goods_files_repository.get(item.id)
            files.append(file.file.dict())

        return files

    def check_files(self, old_files, new_files):
        for item in old_files:
            print(item)
            if not any(item.file_id == int(file['id']) for file in new_files):
                print(item)
                self.goods_files_repository.remove(item)

    @staticmethod
    def parse_images(data):
        images = {}
        for key, value in data.to_dict().items():
            if key.startswith('images'):
                array_ks = key.split('[')
                index = int(array_ks[1].replace(']', ''))
                name = array_ks[2].replace(']', '')

                if not images.get(index, None):
                    images[index] = {}

                images[index][name] = value
        new_images = []
        for item in images:
            new_images.append(images[item])
        return new_images

    def save_new_files(self, files, good_id):
        if len(files):
            for file in files:
                file_id = self.file_service.save_file(files[file], 'goods') or None
                self.goods_files_repository.create(file_id=file_id, good_id=good_id)
