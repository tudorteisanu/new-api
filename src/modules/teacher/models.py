from src.app import db
from datetime import datetime as dt


def get_timestamp():
    return dt.now().isoformat()


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    first_name = db.Column(db.String(128), unique=False, nullable=True)
    last_name = db.Column(db.String(128), unique=False, nullable=True)
    address = db.Column(db.String(256), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    positions = db.relationship("TeacherPosition", cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'Teacher {self.first_name} {self.last_name} - {self.id}'


class TeacherPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id', ondelete='CASCADE'), nullable=True)


