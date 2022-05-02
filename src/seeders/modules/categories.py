from src.modules.categories.models import Category
from datetime import datetime as dt
from src.app import db, app
import requests
from src.modules.file import file_service
from json import dumps
from hashlib import md5
from random import random

data = [
    {
        "name_ro": 'Panouri 3D',
        "name_en": '3D Panels',
        "name_ru": '3Д панэли',
    },
    {
        "name_ro": 'Cornișe',
        "name_en": 'cornices',
        "name_ru": 'карнызы',
    },
    {
        "name_ro": 'muluri',
        "name_en": 'moldings',
        "name_ru": 'молдинги',
    },
    {
        "name_ro": 'seminee',
        "name_en": 'fireplaces',
        "name_ru": 'камины',
    },
    {
        "name_ro": 'Coloane',
        "name_en": 'Columns',
        "name_ru": 'колонны',
    },
    {
        "name_ro": 'tavane',
        "name_en": 'ceilings',
        "name_ru": 'потолки',
    },
    {
        "name_ro": 'cărămizi',
        "name_en": 'bricks',
        "name_ru": 'кирпичи',
    },
    {
        "name_ro": 'Tapete 3D',
        "name_en": '3D carpet',
        "name_ru": '3Д Обои',
    },
    {
        "name_ro": 'vopsele',
        "name_en": 'paints',
        "name_ru": 'краски',
    },
    {
        "name_ro": 'tencuieli',
        "name_en": 'plaster',
        "name_ru": 'штукатурки',
    }
]


class CategoriesSeeder:
    def __init__(self):
        self.fake_url = 'https://picsum.photos/300'
        self.name = __name__


    def __call__(self):
        with app.app_context():
            print('Categories seeder is running..')
            self.create_categories()

    def create_categories(self):
        for item in data:
            category = Category()
            category.name_ro = item['name_ro']
            category.name_en = item['name_en']
            category.name_ru = item['name_ru']
            category.created_at = dt.utcnow().isoformat()
            category.updated_at = dt.utcnow().isoformat()
            category.file_id = self.get_file_id(item)
            category.author_id = None

            db.session.add(category)
            db.session.commit()

    def get_random_file(self, item):
        response = requests.get(self.fake_url)
        filename = f'{md5(dumps(item).encode()).hexdigest()}{random()}.jpg'
        file_path = f'static/categories/{filename}'

        with open(file_path, 'wb') as f:
            f.write(response.content)
            return file_path, filename

    def get_file_id(self, item):
        file_path, filename = self.get_random_file(item)
        return file_service.save_file_from_object(filename, file_path)


categories_seeder = CategoriesSeeder()
