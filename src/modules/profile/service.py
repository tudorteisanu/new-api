from flask import request
from flask import jsonify, g
from src.app.plugins import db
from src.modules.course import Course
from src.modules.teacher.models import TeacherCourse, Teacher
from src.services.http.errors import Success
from datetime import datetime as dt


class ProfileService:
    def show(self):

        resp = {
            "message": 2
        }

        return jsonify(resp)

    def update(self):
        data = request.json
        print(g.user)
        teacher = Teacher.query.filter_by(user_id=g.user.id).first()

        if data.get('courses', None):
            parse_courses(data['courses'], teacher.id)
            
        if data.get('degree_id', None):
            teacher.degree_id = data['degree_id']

        if data.get('position_id', None):
            teacher.position_id = data['position_id']

        db.session.commit()

        return Success()


def parse_courses(courses, teacher_id):
    for course in courses:
        new_course = Course()
        new_course.name = course['name']
        new_course.description = course['description']
        new_course.credits = course['credits']
        new_course.start_date = dt.now().isoformat()
        new_course.end_date = dt.utcnow().isoformat()

        db.session.add(new_course)
        db.session.commit()
        print(new_course, 'new_coursenew_course')

        teacher_course = TeacherCourse(
            teacher_id=teacher_id,
            course_id=new_course.id
        )

        db.session.add(teacher_course)
        db.session.commit()

