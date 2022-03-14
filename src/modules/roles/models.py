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
    alias2 = db.Column(db.String(128), unique=False, nullable=True)
    permissions = db.relationship("RolePermissions", cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'Role {self.name}({self.alias}) - {self.id}'


class RolePermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), nullable=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id', ondelete='CASCADE'), nullable=True)

    def get_permissions(self, role_id):
        return self.query.filter_by(role_id=role_id).all()

    def __repr__(self):
        return f'Role permission {self.role_id}({self.permission_id})'






