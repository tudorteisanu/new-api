from src.modules.users.models import UserRole, User
from src.modules.roles.models import Role
from src.app import db, app

data = [
    {
        "user": "root@domain.com",
        "role": 'admin'
    }
]


class UserRoleSeeder:
    user_seeder = []

    def __init__(self):
        self.user_seeder = []
        self.name = __name__

    def create_items(self):
        for item in data:
            user = User.query.filter_by(email=item['user']).first()
            role = Role.query.filter_by(alias=item['role']).first()

            if user and role and not UserRole.query.filter_by(user_id=user.id, role_id=role.id).first():
                self.user_seeder.append(UserRole(user_id=user.id, role_id=role.id))

    def __call__(self):
        with app.app_context():
            self.create_items()
            print('UserRoleSeeder is running...')
            db.session.add_all(self.user_seeder)
            db.session.commit()


userRoleSeeder = UserRoleSeeder()
