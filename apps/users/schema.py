from settings import ma
from apps.users.models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
