from src.services.utils.repository import Repository
from .models import UserAuthTokens
from src.app import db


class UserTokenRepository(UserAuthTokens, Repository):
    @staticmethod
    def create(**kwargs):
        model = UserAuthTokens(**kwargs)
        db.session.add(model)
        db.session.commit()
        return model
