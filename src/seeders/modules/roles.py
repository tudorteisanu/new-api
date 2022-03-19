from src.modules.roles.models import Role

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
        for item in data:
            if not (Role.query.filter_by(name=item['name'], alias=item['alias']).first()):
                self.roles_seeder.append(Role(name=item['name'], alias=item['alias']))


    def __call__(self):
        return self.roles_seeder


roles_seeder = RolesSeeder()
