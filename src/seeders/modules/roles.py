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

roles_seeder = []

for item in data:
    roles_seeder.append(Role(name=item['name'], alias=item['alias']))
