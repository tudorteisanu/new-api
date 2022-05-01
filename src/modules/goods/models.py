from sqlalchemy.orm import backref

from src.app import db
from datetime import datetime as dt
from flask import g


def set_author():
    if hasattr(g, 'user'):
        return g.user.id
    return None


def get_timestamp():
    return dt.now().isoformat()


class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    name_ro = db.Column(db.String(128), unique=False, nullable=True)
    name_en = db.Column(db.String(128), unique=False, nullable=True)
    name_ru = db.Column(db.String(128), unique=False, nullable=True)
    description_ro = db.Column(db.Text, unique=False, nullable=True)
    description_en = db.Column(db.Text, unique=False, nullable=True)
    description_ru = db.Column(db.Text, unique=False, nullable=True)
    height = db.Column(db.Float())
    width = db.Column(db.Float())
    length = db.Column(db.Float())
    price = db.Column(db.Float())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, default=set_author)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id', ondelete='CASCADE'), nullable=True)
    image = db.relationship("File", backref=backref("good_image", uselist=False))
    category = db.relationship("Category", backref=backref("good_category", uselist=False))

    def __repr__(self):
        return f'Category - {self.id}'
