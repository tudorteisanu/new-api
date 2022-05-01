from flask import jsonify, g
from src.app.plugins import db
from src.services.http.errors import Success
from src.services.http.errors import UnprocessableEntity
from src.services.http.errors import NotFound
from .serializer import ProfileSerializer

from src.modules.teacher.repository import TeacherRepository
from src.modules.teacher.repository import TeacherDetailsRepository
from src.modules.teacher.repository import TeacherCourseRepository
from src.modules.teacher.repository import TeacherPositionsRepository


class ProfileService:
    def __init__(self):
        self.teacher_repository = TeacherRepository()
        self.teacher_positions_repository = TeacherPositionsRepository()
        self.teacher_course_repository = TeacherCourseRepository()
        self.teacher_detail_repository = TeacherDetailsRepository()

    def show(self, user_id=None):
        if not user_id:
            user_id = g.user.id

        teacher = self.teacher_repository.find_one(user_id=user_id)

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
            "details": self.get_details(teacher.id)
        }

        return jsonify(resp)

    def update(self, data, user_id=None):
        if not user_id:
            user_id = g.user.id

        serializer = ProfileSerializer(data=data)

        if not serializer.is_valid():
            return UnprocessableEntity(errors=serializer.errors)

        teacher = self.teacher_repository.find_one(user_id=user_id)

        if not teacher:
            teacher = self.teacher_repository.create(user_id=user_id)

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

    def get_teacher_courses(self, teacher_id):
        courses = self.teacher_course_repository.find(teacher_id=teacher_id)

        return [{
            "id": item.id,
            "dates": item.dates,
            "credits": item.credits,
            "name": item.name,
            "description": item.description,
        } for item in courses]

    def get_teacher_positions(self, teacher_id):
        positions = self.teacher_positions_repository.find(teacher_id=teacher_id)
        return [{
            "id": item.id,
            "position_id": item.position_id,
            "degree_id": item.degree_id,
            "work_experience": item.work_experience,
        } for item in positions]

    def update_details(self, details, teacher_id):
        old_details = self.teacher_detail_repository.find(teacher_id=teacher_id)

        for item in old_details:
            if not any(el.get('id', None) == item.id for el in details):
                db.session.delete(item)
                db.session.commit()

        for item in details:
            if item.get('id', None):
                detail = self.teacher_detail_repository.get(item['id'])

                if not detail:
                    detail = self.teacher_detail_repository.create(teacher_id=teacher_id)

            else:
                detail = self.teacher_detail_repository.create(teacher_id=teacher_id)

            self.teacher_detail_repository.update(detail, {
                "title": item.get('title', ''),
                "dates": item.get('dates', []),
                "credits": item.get('credits', None)
            })

            db.session.commit()

    def update_positions(self, positions, teacher_id):
        old_positions = self.teacher_positions_repository.find(teacher_id=teacher_id)

        for item in old_positions:
            if not any(el.get('id', None) == item.id for el in positions):
                db.session.delete(item)
                db.session.commit()

        for item in positions:
            if item.get('id', None):
                position = self.teacher_positions_repository.get(item['id'])

                if not position:
                    position = self.teacher_positions_repository.create(teacher_id=teacher_id)

            else:
                position = self.teacher_positions_repository.create(teacher_id=teacher_id)

            self.teacher_positions_repository.update(position, {
                "position_id": item['position_id'],
                "degree_id": item['degree_id'],
                "work_experience": item['work_experience']
            })

        db.session.commit()

    def update_courses(self, positions, teacher_id):
        old_data = self.teacher_course_repository.find(teacher_id=teacher_id)

        for item in old_data:
            if not any(el.get('id', None) == item.id for el in positions):
                db.session.delete(item)
                db.session.commit()

        for item in positions:
            if item.get('id', None):
                course = self.teacher_course_repository.get(item['id'])

                if not course:
                    course = self.teacher_course_repository.create(teacher_id=teacher_id)

            else:
                course = self.teacher_course_repository.create(teacher_id=teacher_id)

            self.teacher_course_repository.update(course, {
                "dates": item.get('dates', []),
                "credits": item.get('credits', None),
                "name": item.get('name', ''),
                "description": item.get('description', ''),
            })

        db.session.commit()

    def get_details(self, teacher_id):
        return [
            {
                "id": item.id,
                "title": item.title,
                "dates": item.dates,
                "credits": item.credits
            } for item in self.teacher_detail_repository.find(teacher_id=teacher_id)
        ]

    @staticmethod
    def update_teacher(model, data):
        if data.get('address', None):
            model.address = data['address']

        if data.get('phone', None):
            model.phone = data['phone']
