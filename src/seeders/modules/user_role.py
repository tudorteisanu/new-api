from src.modules.users.models import UserRole, User
from src.modules.roles.models import Role


class UserRoleSeeder:
    def __call__(self):
        user = User.query.filter_by(email='teisanutudort@gmail.com').first()
        role = Role.query.filter_by(alias='admin').first()

        if user and role:
            return [UserRole(user_id=user.id, role_id=role.id)]

        return []


userRoleSeeder = UserRoleSeeder()
