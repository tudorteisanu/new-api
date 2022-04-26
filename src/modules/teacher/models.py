from src.app import db
from datetime import datetime as dt
from sqlalchemy.orm import backref


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
    user = db.relationship("User", backref=backref("teacher_user", uselist=False))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id', ondelete='CASCADE'), nullable=True)
    position = db.relationship("Position", backref=backref("teacher_position", uselist=False))
    degree_id = db.Column(db.Integer, db.ForeignKey('degree.id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return f'Teacher {self.first_name} {self.last_name} - {self.id}'


class TeacherCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=get_timestamp)
    updated_at = db.Column(db.DateTime, default=get_timestamp)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=True)


