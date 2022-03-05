from src.app import db
from datetime import datetime as dt


def get_timestamp():
    return dt.now().isoformat()


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    credits = db.Column(db.Integer, unique=False, nullable=True)
    description = db.Column(db.String(256), unique=False, nullable=True)
    name = db.Column(db.String(128), unique=False, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return f'Course {self.name} - {self.id}'
