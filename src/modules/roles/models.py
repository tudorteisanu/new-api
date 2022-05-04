from src.app import db
from datetime import datetime as dt


def get_timestamp():
    return dt.now().isoformat()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    name = db.Column(db.String(128))
    alias = db.Column(db.String(128), unique=True, nullable=False)
    permissions = db.relationship("RolePermissions", cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'Role {self.name}({self.alias}) - {self.id}'


class RolePermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), nullable=False)
    endpoint = db.Column(db.String, nullable=False)
    method = db.Column(db.String, nullable=False)

    def get_permissions(self, role_id):
        return self.query.filter_by(role_id=role_id).all()

    def __repr__(self):
        return f'{self.method}: ({self.endpoint} - {self.role_id}'






