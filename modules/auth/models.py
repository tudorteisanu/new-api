from config.settings import db
from datetime import datetime as dt


def get_timestamp():
    now = dt.now().timestamp()
    time = str(now).split('.')[0]
    return int(time)


class UserAuthTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    access_token = db.Column(db.String(512), nullable=True)

    def set_token(self, token):
        self.access_token = token

    def remove_token(self):
        self.access_token = None

