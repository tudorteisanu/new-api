from src.app import db
from src.seeders.modules.roles import roles_seeder

seeders = [*roles_seeder]


def seed_db():
    try:
        db.session.add_all(seeders)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
