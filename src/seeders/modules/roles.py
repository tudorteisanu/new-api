from src.modules.roles.models import Role
from src.app import db, app

data = [
    {
        "name": "Admin",
        "alias": 'admin'
    },
    {
        "name": "Guest",
        "alias": 'guest'
    }
]


class RolesSeeder:
    roles_seeder = []

    def __init__(self):
        self.roles_seeder = []
        self.name = __name__

    def __call__(self):
        with app.app_context():
            print("RolesSeeder is running...")
            for item in data:
                if not (Role.query.filter_by(name=item['name'], alias=item['alias']).first()):
                    self.roles_seeder.append(Role(name=item['name'], alias=item['alias']))
            db.session.add_all(self.roles_seeder)
            db.session.commit()


roles_seeder = RolesSeeder()
