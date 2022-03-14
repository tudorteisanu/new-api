from src.app import db
from src.seeders.modules.roles import roles_seeder
from src.seeders.modules.users import users_seeder
from src.seeders.modules.user_role import userRoleSeeder


def seed_db():
    try:
        db.session.add_all([
            *roles_seeder(),
            *users_seeder()
        ])
        db.session.commit()
        db.session.add_all([*userRoleSeeder()])
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
