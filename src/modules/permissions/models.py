import logging

from src.app import db
from datetime import datetime as dt


def get_timestamp():
    return dt.now().isoformat()


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    name = db.Column(db.String(128))
    alias = db.Column(db.String(128), unique=True, nullable=False)

    class Meta:
        permissions = [
            ("Get all permissions", 'permissions.index'),
            ("Add permissions", 'permissions.store'),
            ("Get one permission", 'permissions.get'),
            ('Update permission', 'permissions.update'),
            ('Delete permission', 'permissions.delete'),
            ("Permissions list", 'permissions.list'),
            ("Permissions list", 'permissions.list'),
        ]

    def __repr__(self):
        return f'Permission {self.name}({self.alias}) - {self.id}'


class BasePermissions:
    __abstract__ = True

    def __call__(cls):
        try:
            new_permissions = []
            for item in cls.Meta.permissions:
                if Permission.query.filter_by(alias=item[1]).first() is None:
                    print(item)
                    new_permissions.append(Permission(name=item[0], alias=item[1]))
            db.session.add_all(new_permissions)
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
