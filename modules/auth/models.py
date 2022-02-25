from application import db
from datetime import datetime as dt


def get_timestamp():
    return dt.now().isoformat()


class UserAuthTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, )
    access_token = db.Column(db.String(512), nullable=True)

    def set_token(self, token):
        self.access_token = token

    def remove_token(self):
        self.access_token = None
