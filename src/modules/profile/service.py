from flask import request
from flask import jsonify, g
from src.app.plugins import db
from src.modules.course import Course
from src.modules.teacher.models import TeacherCourse, Teacher, TeacherDetails
from src.modules.teacher.models import TeacherPositions
from src.services.http.errors import Success
from src.services.http.errors import UnprocessableEntity
from .serializer import ProfileSerializer
from datetime import datetime as dt


class ProfileService:
    def show(self):

        teacher = Teacher.query.filter_by(user_id=g.user.id).first()
        if not teacher:
            teacher = Teacher()
            db.session.commit()

        courses = self.get_teacher_courses(teacher.id)

        resp = {
            "courses": self.__parse_courses(courses),
            "details": self.get_details(teacher.id) if teacher else {}
        }

        return jsonify(resp)

    def update(self):
        data = request.json
        serializer = ProfileSerializer(data=data)

        if not serializer.is_valid():
            return UnprocessableEntity(errors=serializer.errors)

        teacher = Teacher.query.filter_by(user_id=g.user.id).first()

        if not teacher:
            teacher = Teacher(user_id=g.user.id)
            db.session.add(teacher)

        if data.get('address', None):
            teacher.address = data['address']

        if data.get('phone', None):
            teacher.phone = data['phone']

        if data.get('courses', None):
            self.update_courses(data['courses'], teacher.id)

        if data.get('positions', None):
            self.update_positions(data['positions'], teacher.id)

        if data.get('details', None):
            self.update_details(data['details'], teacher.id)

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

    @staticmethod
    def get_teacher_courses(teacher_id):
        courses_ids = [item.course_id for item in TeacherCourse.query.filter_by(teacher_id=teacher_id).all()]
        return Course.query.filter(Course.id.in_(courses_ids)).all()

    def update_courses(self, courses, teacher_id):
        old_courses = self.get_teacher_courses(teacher_id)

        for course in old_courses:
            if not any(x.get('id', None) == course.id for x in courses):
                db.session.delete(course)

        old_courses = self.get_teacher_courses(teacher_id)

        for course in courses:
            if not any(item.id == course.get('id', None) for item in old_courses):
                new_course = Course()
                new_course.name = course['name']
                new_course.description = course['description']
                new_course.credits = course['credits']
                new_course.dates = course.get('dates', None) or []
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
            else:
                new_course = Course.query.get(course.get('id'))
                new_course.name = course['name']
                new_course.description = course['description']
                new_course.dates = course.get('dates', None) or []
                new_course.credits = course['credits']

    @staticmethod
    def update_details(details, teacher_id):
        old_details = TeacherDetails.query.filter_by(teacher_id=teacher_id).all()

        # for course in old_details:
        #     if not any(x.get('id', None) == course.id for x in details):
        #         db.session.delete(course)

        for detail in details:
            if detail.get('id', None) is None:
                new_detail = TeacherDetails()
                new_detail.teacher_id = teacher_id
                db.session.add(new_detail)
                db.session.commit()
            else:
                new_detail = TeacherDetails.query.get(detail['id'])

            new_detail.title = detail['title']
            new_detail.dates = detail.get('dates') or None
            new_detail.credits = detail['credits']

            db.session.commit()

    @staticmethod
    def update_positions(positions, teacher_id):
        old_positions = TeacherDetails.query.filter_by(teacher_id=teacher_id).all()

        for item in old_positions:
            if not any(el.get('id', None) == item.id for el in positions):
                db.session.delete(item)

        for item in positions:
            if item.get('id', None):
                position = TeacherPositions.query.get(item['id'])

                if not position:
                    position = TeacherPositions(teacher_id=teacher_id)
                    db.session.add(position)

            else:
                position = TeacherPositions(teacher_id=teacher_id)
                db.session.add(position)

            position.position_id = item['position_id']
            position.degree_id = item['degree_id']
            position.work_experience = item['work_experience']

        db.session.commit()

    @staticmethod
    def get_details(teacher_id):
        return [
            {
                "id": item.id,
                "title": item.title,
                "date": item.date
            } for item in TeacherDetails.query.filter_by(teacher_id=teacher_id).all()
        ]
