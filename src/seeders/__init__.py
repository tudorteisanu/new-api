from src.app import db
from src.seeders.modules.roles import roles_seeder
from src.seeders.modules.users import users_seeder
from .modules.categories import categories_seeder
from .modules.goods import goods_seeder
from datetime import datetime as dt


class Timer:
    def __init__(self):
        self.start_time = dt.now()

    def stop(self):
        return (dt.now() - self.start_time).total_seconds()


def seed_db():
    try:
        seeders = [
            roles_seeder,
            users_seeder,
            # categories_seeder,
            # goods_seeder
        ]

        print('-------------------- Starts seed Database. --------------------')

        for seeder in seeders:
            timer = Timer()
            seeder()
            print(f'{seeder.__class__.__name__} seeder executed in: {timer.stop()}')

        print('-------------------- All seeders executed. --------------------')
    except Exception as e:
        print(e)
        db.session.rollback()
