from flask_login import UserMixin
from config.settings import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from modules.auth.models import UserAuthTokens
from services.database import Base


def get_timestamp():
    return dt.now().isoformat()


class User(UserMixin, Base):
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(128))
    role = db.Column(db.String(12), server_default='user')
    reset_code = db.Column(db.String, server_default='')
    confirmed_at = db.Column(db.DateTime)
    login_attempts = db.Column(db.Integer, default=3)
    login_blocked_time = db.Column(db.DateTime)
    reset_password_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, server_default='False')
    token = db.relationship("UserAuthTokens", uselist=False, cascade='all, delete, delete-orphan')

    def __repr__(self):
        return 'User {} - {}'.format(self.email, self.id)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.commit()
        return self.password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create_token(self):
        token = create_access_token(self.id)
        user_token = UserAuthTokens()
        user_token = user_token.find_one(user_id=self.id)

        if user_token:
            user_token.update({"access_token": token})
        else:
            user_token = UserAuthTokens()
            user_token.create({"user_id": self.id, "access_token": token})
        return token

    def create_access_token(self):
        user_token = UserAuthTokens.query.filter_by(user_id=self.id).first()

        if not user_token:
            user_token = UserAuthTokens()
            user_token.create({"user_id": self.id})

    def remove_token(self):
        user_token = UserAuthTokens()
        user_token = user_token.find_one(user_id=self.id)
        user_token.update({"access_token": None})


UserResource = User()