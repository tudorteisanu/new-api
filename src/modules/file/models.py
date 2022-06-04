from src.app import db
from datetime import datetime as dt
from flask import g
from os import environ
from dotenv import load_dotenv

load_dotenv('.env')


def set_author():
    if hasattr(g, 'user'):
        return g.user.id
    return None


def get_timestamp():
    return dt.now().isoformat()


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    name = db.Column(db.String(128), unique=False, nullable=True)
    path = db.Column(db.String(128), unique=False, nullable=True)
    mime_type = db.Column(db.String(128), unique=False, nullable=True)
    size = db.Column(db.Integer, unique=False, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, default=set_author)

    def __repr__(self):
        return f'File - {self.name}'

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "url": f'{environ.get("STATIC_PATH", "")}/{self.path}'
        }

    def get_url(self):
        if self.path is None:
            return ""
        return f'{environ.get("STATIC_PATH", "")}/{self.path}'

