from modules.users.models import User
from marshmallow_sqlalchemy import ModelSchema, fields
from modules.auth.schema import UserAuthTokensSchema


class UserSchema(ModelSchema):
    class Meta:
        model = User

    token = fields.Nested(UserAuthTokensSchema(only=['access_token']), many=False)
