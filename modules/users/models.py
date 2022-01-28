from flask_login import UserMixin
from config.settings import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from modules.auth.models import UserAuthTokens


def get_timestamp():
    return dt.now().isoformat()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(128))
    role = db.Column(db.String(12), server_default='user')
    reset_code = db.Column(db.String, server_default='')
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    confirmed_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, server_default='False')
    token = db.relationship("UserAuthTokens", uselist=False, cascade='all, delete, delete-orphan')

    def create(self, data, exclude=None):
        if exclude is None:
            exclude = ['password_hash', 'token', "id", 'reset_code']

        for (key, value) in data.items():
            if hasattr(self, key) and key not in exclude:
                setattr(self, key, value)
        self.hash_password(data.get('password'))
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return 'User {} - {}'.format(self.email, self.id)

    def update(self, data, exclude=None):
        if exclude is None:
            exclude = ['password_hash']

        for (key, value) in data.items():
            if hasattr(self, key) and key not in exclude:
                setattr(self, key, value)
        self.updated_at = get_timestamp()
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

    def remove_token(self):
        user_token = UserAuthTokens.query.filter_by(user_id=self.id).first()
        user_token.access_token = None
        db.session.commit()
