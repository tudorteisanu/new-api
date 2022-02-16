from modules.auth.models import UserAuthTokens
from config.settings import ma


class UserAuthTokensSchema(ma.Schema):
    class Meta:
        model = UserAuthTokens
