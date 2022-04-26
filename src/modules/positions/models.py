from src.app import db
from datetime import datetime as dt


def get_timestamp():
    return dt.now().isoformat()


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    name = db.Column(db.String(128), unique=False, nullable=True)

    def __repr__(self):
        return f'Position {self.name} - {self.id}'
