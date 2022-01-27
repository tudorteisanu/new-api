from datetime import datetime
from datetime import timedelta
import random

from flask_login import UserMixin
from sqlalchemy.orm import backref

from config.flask_config import FlaskConfig
from services.mail import send_email_link
from config.settings import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from modules.auth.models import UserAuthTokens


def get_timestamp():
    now = dt.now().timestamp()
    time = str(now).split('.')[0]
    return int(time)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(128))
    role = db.Column(db.String(12), server_default='user')
    reset_code = db.Column(db.String, server_default='')
    reset_code_expire = db.Column(db.DateTime, server_default=None)
    token = db.relationship("UserAuthTokens", uselist=False)

    def __init__(self, data, exclude=['password_hash', 'token', "id", 'reset_code', 'reset_code_expire']):
        for (key, value) in data.items():
            if hasattr(self, key) and key not in exclude:
                setattr(self, key, value)
        self.hash_password(data.get('password'))
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return 'User {} - {}'.format(self.email, self.id)

    def update(self, data, exclude=['password_hash']):
        for (key, value) in data.items():
            if hasattr(self, key) and key not in exclude:
                setattr(self, key, value)
        db.session.commit()

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create_token(self):
        token = create_access_token(self.id)
        user_token = UserAuthTokens.query.filter_by(user_id=self.id).first()
        if user_token:
            user_token.set_token(token)
            db.session.commit()
        else:
            user_token = UserAuthTokens(user_id=self.id, access_token=token)
            db.session.add(user_token)
            db.session.commit()
        return token

    def create_access_token(self):
        user_token = UserAuthTokens.query.filter_by(user_id=self.id).first()

        if not user_token:
            user_token = UserAuthTokens(user_id=self.id)
            db.session.add(user_token)
            db.session.commit()

    def remove_expired_token(self):
        self.reset_code = None
        self.reset_code_expire = None

    def generate_reset_password_code(self):
        token = random.getrandbits(128)
        link = f'{FlaskConfig.FRONTEND_ADDRESS}/reset_password?token={token}'
        self.reset_code = token
        self.reset_code_expire = datetime.now() + timedelta(minutes=60)
        send_email_link(self.email, link)

    def remove_token(self):
        user_token = UserAuthTokens.query.filter_by(user_id=self.id).first()
        user_token.access_token = None
        db.session.commit()
