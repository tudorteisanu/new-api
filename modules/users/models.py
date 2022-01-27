from datetime import datetime
from datetime import timedelta
import random

from flask_login import UserMixin

from config.flask_config import FlaskConfig
from config.mail import send_email_link
from config.settings import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


def get_timestamp():
    now = dt.now().timestamp()
    time = str(now).split('.')[0]
    return int(time)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(128))
    role = db.Column(db.String(12), server_default='user')
    reset_code = db.Column(db.String, server_default='')
    reset_code_expire = db.Column(db.DateTime, server_default=None)

    def __repr__(self):
        return 'User {} - {}'.format(self.email, self.id)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create_token(self):
        return create_access_token(self.id)

    def remove_expired_token(self):
        self.reset_code = None
        self.reset_code_expire = None

    def generate_reset_password_code(self):
        token = random.getrandbits(128)
        link = f'{FlaskConfig.FRONTEND_ADDRESS}/reset_password?token={token}'
        self.reset_code = token
        self.reset_code_expire = datetime.now() + timedelta(minutes=60)
        send_email_link(self.email, link)
