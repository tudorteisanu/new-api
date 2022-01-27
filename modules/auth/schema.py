from modules.auth.models import UserAuthTokens
from marshmallow_sqlalchemy import ModelSchema


class UserAuthTokensSchema(ModelSchema):
    class Meta:
        model = UserAuthTokens
