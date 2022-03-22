from src.modules.users.models import User
from datetime import datetime as dt
from src.app import db, app

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
        self.users_seeder = []
        self.name = __name__

    def create_users(self):
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
        with app.app_context():
            print("UsersSeeder is running...")
            self.create_users()
            db.session.add_all(self.users_seeder)
            db.session.commit()


users_seeder = UsersSeeder()
