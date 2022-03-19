from src.modules.users.models import User
from datetime import datetime as dt
data = [
    {
        "name": "Root",
        "email": 'root@domain.com',
        "password": "12345678"
    }
]


class UsersSeeder:
    users_seeder = []

    def __init__(self):
        for item in data:
            if not User.query.filter_by(email=item['email']).first():
                user = User()
                user.name = item['name']
                user.email = item['email']
                user.is_active = True
                user.confirmed_at = dt.now().isoformat()
                user.password_hash = user.hash_password(item['password'])
                self.users_seeder.append(user)

    def __call__(self):
        return self.users_seeder


users_seeder = UsersSeeder()
