from config.settings import db
from services.database import Base


class UserAuthTokens(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, )
    access_token = db.Column(db.String(512), nullable=True)

    def set_token(self, token):
        self.access_token = token

    def remove_token(self):
        self.access_token = None
