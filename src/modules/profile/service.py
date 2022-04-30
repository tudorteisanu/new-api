from flask import request
from flask import jsonify, g
from src.app.plugins import db
from src.modules.teacher.models import TeacherCourse, Teacher, TeacherDetails
from src.modules.teacher.models import TeacherPositions
from src.services.http.errors import Success
from src.services.http.errors import UnprocessableEntity
from src.services.http.errors import NotFound
from .serializer import ProfileSerializer


class ProfileService:
    def show(self, user_id=None):
        if not user_id:
            user_id = g.user.id

        teacher = Teacher.query.filter_by(user_id=user_id).first()

        if not teacher:
            return NotFound(message="Teacher not found")

        resp = {
            "teacher": {
                "address": teacher.address,
                "id": teacher.id,
                "phone": teacher.phone,
                "first_name": teacher.first_name,
                "last_name": teacher.last_name,
            },
            "courses": self.get_teacher_courses(teacher.id),
            "positions": self.get_teacher_positions(teacher.id),
            "details": self.get_details(teacher.id) if teacher else {}
        }

        return jsonify(resp)

    def update(self, user_id=None):
        if not user_id:
            user_id = g.user.id

        data = request.json
        serializer = ProfileSerializer(data=data)

        if not serializer.is_valid():
            return UnprocessableEntity(errors=serializer.errors)

        teacher = Teacher.query.filter_by(user_id=user_id).first()

        if not teacher:
            teacher = Teacher(user_id=user_id)
            db.session.add(teacher)
            db.session.commit()

        if data.get('teacher', None):
            self.update_teacher(teacher, data['teacher'])

        if data.get('courses', None):
            self.update_courses(data['courses'], teacher.id)

        if data.get('positions', None):
            self.update_positions(data['positions'], teacher.id)

        if data.get('details', None):
            self.update_details(data['details'], teacher.id)

        db.session.commit()

        return Success()

    @staticmethod
    def get_teacher_courses(teacher_id):
        courses = TeacherCourse.query.filter_by(teacher_id=teacher_id).all()

        return [{
            "id": item.id,
            "dates": item.dates,
            "credits": item.credits,
            "name": item.name,
            "description": item.description,
        } for item in courses]

    @staticmethod
    def get_teacher_positions(teacher_id):
        positions = TeacherPositions.query.filter_by(teacher_id=teacher_id).all()
        return [{
            "id": item.id,
            "position_id": item.position_id,
            "degree_id": item.degree_id,
            "work_experience": item.work_experience,
        } for item in positions]

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
    def update_courses(positions, teacher_id):
        old_data = TeacherCourse.query.filter_by(teacher_id=teacher_id).all()

        for item in old_data:
            if not any(el.get('id', None) == item.id for el in positions):
                db.session.delete(item)

        for item in positions:
            if item.get('id', None):
                course = TeacherCourse.query.get(item['id'])

                if not course:
                    course = TeacherCourse(teacher_id=teacher_id)
                    db.session.add(course)

            else:
                course = TeacherCourse(teacher_id=teacher_id)
                db.session.add(course)

            course.dates = item.get('dates', [])
            course.credits = item.get('credits', None)
            course.name = item.get('name', '')
            course.description = item.get('description', '')

        db.session.commit()

    @staticmethod
    def get_details(teacher_id):
        return [
            {
                "id": item.id,
                "title": item.title,
                "dates": item.dates,
                "credits": item.credits
            } for item in TeacherDetails.query.filter_by(teacher_id=teacher_id).all()
        ]

    @staticmethod
    def update_teacher(model, data):
        if data.get('address', None):
            model.address = data['address']

        if data.get('phone', None):
            model.phone = data['phone']
