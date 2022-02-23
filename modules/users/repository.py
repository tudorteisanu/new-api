from modules.users.models import User


class UserRepository(User):
    def find(self):
        return self.query.all()

    def find_one(self, user_id):
        return self.query.get(user_id)

    def list(self):
        return [{"value": item.id, "text": item.name, "email": item.email} for item in self.query.all()]


userRepository = UserRepository()
