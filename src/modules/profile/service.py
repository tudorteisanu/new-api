from flask import request
from flask import jsonify, g
from src.app.plugins import db
from src.modules.course import Course
from src.modules.teacher.models import TeacherCourse, Teacher
from src.services.http.errors import Success
from datetime import datetime as dt


class ProfileService:
    def show(self):

        teacher = Teacher.query.filter_by(user_id=g.user.id).first()
        courses_ids = [item.course_id for item in TeacherCourse.query.filter_by(teacher_id=teacher.id).all()]

        courses = Course.query.filter(Course.id.in_(courses_ids)).all()

        resp = {
            "position_id": teacher.position_id,
            "degree_id": teacher.degree_id,
            "courses": self.__parse_courses(courses)
        }

        return jsonify(resp)

    @staticmethod
    def update():
        data = request.json

        teacher = Teacher.query.filter_by(user_id=g.user.id).first()
        print(teacher.id)
        if data.get('courses', None):
            update_courses(data['courses'], teacher.id)
            
        if data.get('degree_id', None):
            teacher.degree_id = data['degree_id']

        if data.get('position_id', None):
            teacher.position_id = data['position_id']

        db.session.commit()

        return Success()

    @staticmethod
    def __parse_courses(courses):
        return [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "credits": item.credits,
                "start_date": item.start_date,
            } for item in courses
        ]


def update_courses(courses, teacher_id):
    for course in courses:
        new_course = Course()
        new_course.name = course['name']
        new_course.description = course['description']
        new_course.credits = course['credits']
        new_course.start_date = dt.now().isoformat()
        new_course.end_date = dt.utcnow().isoformat()

        db.session.add(new_course)
        db.session.commit()

        teacher_course = TeacherCourse(
            teacher_id=teacher_id,
            course_id=new_course.id
        )

        db.session.add(teacher_course)
        db.session.commit()

