from config.settings import app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from datetime import datetime as dt

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def get_timestamp():
    return dt.now().isoformat()


class Fields:
    def string(*args, **kwargs):
        return db.Column(db.String(*args), **kwargs)

    def integer(*args, **kwargs):
        return db.Column(db.Integer, *args, **kwargs)

    def boolean(*args, **kwargs):
        return db.Column(db.Boolean(*args), **kwargs)

    def date(*args, **kwargs):
        return db.Column(db.DateTime(*args), **kwargs)

    def relationship(*args, **kwargs):
        return db.relationship(*args, **kwargs)

    def foreign_key(*args, **kwargs):
        return db.ForeignKey(*args, **kwargs)

    def column(*args, **kwargs):
        return db.Column(*args, **kwargs)

    Integer = db.Integer
    String = db.String
    Boolean = db.Boolean
    Text = db.Text
    JSONB = JSONB


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    blocked_columns = ['created_at', 'updated_at']
    db = db

    def __repr__(self):
        return f'{__name__} - {self.id}'

    def filter(self, **kwargs):
        try:
            return self.query.filter(**kwargs)
        except Exception as e:
            raise e

    def find_one(self, **kwargs):
        try:
            return self.query.filter_by(**kwargs).first()
        except Exception as e:
            raise e

    def find(self, **kwargs):
        try:
            return self.query.filter_by(**kwargs).all()
        except Exception as e:
            raise e

    def get(self, query):
        try:
            return self.query.get(query)
        except Exception as e:
            raise e

    def update(self, data, exclude=[]):
        exclude = [*exclude, *self.blocked_columns]
        try:
            for (key, value) in data.items():
                if hasattr(self, key) and key not in exclude:
                    setattr(self, key, value)

            self.updated_at = get_timestamp()
            db.session.commit()
            return self
        except Exception as e:
            raise e

    def create(self, data, exclude=[]):
        exclude = [*exclude, *self.blocked_columns]

        try:
            for (key, value) in data.items():
                if hasattr(self, key) and key not in exclude:
                    setattr(self, key, value)

            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            raise e
