from src.modules.goods.models import Good
from src.modules.categories.models import Category
from datetime import datetime as dt
from src.app import db, app
import requests
from src.modules.file import file_service
from json import dumps
from hashlib import md5
from random import random, randint, choice
from faker import Faker


class GoodsSeeder:
    items = []
    fake_url = 'https://picsum.photos/300'

    def __init__(self):
        self.name = __name__


    def __call__(self, count=500):
        with app.app_context():
            print('Goods seeder is running..')
            self.seed_goods(count)


    def seed_goods(self, count):
        categories = [item[0] for item in Category.query.with_entities(Category.id).all()]

        for item in range(count):
            faker_ro = Faker('ro_RO')
            name_ro = faker_ro.name()
            text_ro = faker_ro.text()

            faker_en = Faker('en_US')
            name_en = faker_en.name()
            text_en = faker_en.text()

            faker_ru = Faker('ru_RU')
            name_ru = faker_ru.name()
            text_ru = faker_ru.text()

            good = Good()
            good.name_ro = name_ro
            good.name_en = name_en
            good.name_ru = name_ru
            good.description_en = text_en
            good.description_ru = text_ru
            good.description_ro = text_ro
            good.height = randint(100, 1000)
            good.width = randint(100, 900)
            good.length = randint(100, 400)
            good.price = randint(100, 10000)
            good.created_at = dt.utcnow().isoformat()
            good.updated_at = dt.utcnow().isoformat()
            good.file_id = self.get_file_id(item)
            good.category_id = choice(categories)
            good.author_id = None

            db.session.add(good)
            db.session.commit()

    def get_random_file(self, item):
        response = requests.get(self.fake_url)
        filename = f'{md5(dumps(item).encode()).hexdigest()}{random()}.jpg'
        file_path = f'static/goods/{filename}'
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
            return file_path, filename

    def get_file_id(self, item):
        file_path, filename = self.get_random_file(item)
        return file_service.save_file_from_object(filename, file_path)


goods_seeder = GoodsSeeder()
