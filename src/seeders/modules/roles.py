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

    def __call__(self):
        for item in data:
            self.roles_seeder.append(Role(name=item['name'], alias=item['alias']))

        return self.roles_seeder


roles_seeder = RolesSeeder()
