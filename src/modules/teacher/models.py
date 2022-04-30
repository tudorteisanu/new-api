from src.app import db
from datetime import datetime as dt
from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import JSONB


def get_timestamp():
    return dt.now().isoformat()


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    first_name = db.Column(db.String(128), unique=False, nullable=True)
    last_name = db.Column(db.String(128), unique=False, nullable=True)
    address = db.Column(db.String(256), unique=False, nullable=True)
    phone = db.Column(db.String(15), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    user = db.relationship("User", backref=backref("teacher_user", uselist=False))
    positions = db.relationship("TeacherPositions", backref=backref("teacher_positions"))

    def __repr__(self):
        return f'Teacher {self.first_name} {self.last_name} - {self.id}'


class TeacherCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    dates = db.Column(JSONB, default=[])
    credits = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)
    name = db.Column(db.String, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=True)


class TeacherDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    dates = db.Column(JSONB, default=[])
    title = db.Column(db.Text, nullable=True)
    credits = db.Column(db.Float, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=True)


class TeacherPositions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id', ondelete='CASCADE'), nullable=True)
    degree_id = db.Column(db.Integer, db.ForeignKey('degree.id', ondelete='CASCADE'), nullable=True)
    work_experience = db.Column(db.Float, nullable=True)



