from app import db
from datetime import datetime as dt


def get_timestamp():
    return dt.now().isoformat()


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    name_ro = db.Column(db.String(64), unique=True, nullable=True)
    name_ru = db.Column(db.String(64), unique=True, nullable=True)
    name_en = db.Column(db.String(64), unique=True, nullable=True)

    def __repr__(self):
        return 'Position {} - {}'.format(self.name, self.id)
