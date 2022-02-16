from modules.users.models import User
from config.settings import ma
from modules.auth.schema import UserAuthTokensSchema


class UserSchema(ma.Schema):
    class Meta:
        model = User

    token = ma.Nested(UserAuthTokensSchema(many=False))
