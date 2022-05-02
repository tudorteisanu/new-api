import logging

from flask import jsonify, g
from src.app.plugins import db
from src.services.http.response import Success

from src.modules.teacher.repository import TeacherRepository
from src.modules.teacher.repository import TeacherDetailsRepository
from src.modules.teacher.repository import TeacherCourseRepository
from src.modules.teacher.repository import TeacherPositionsRepository

from src.exceptions.http import UnknownError
from src.exceptions.http import NotFoundException
from src.exceptions.http import ValidationError

from .serializer import ProfileSerializer


class ProfileService:
    def __init__(self):
        self.teacher_repository = TeacherRepository()
        self.teacher_positions_repository = TeacherPositionsRepository()
        self.teacher_course_repository = TeacherCourseRepository()
        self.teacher_detail_repository = TeacherDetailsRepository()

    def show(self, user_id=None):
        try:
            if not user_id:
                user_id = g.user.id

            teacher = self.teacher_repository.find_one(user_id=user_id)

            if not teacher:
                raise NotFoundException(message="Teacher not found")

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
        except Exception as e:
            raise UnknownError(e)

    def update(self, data, user_id=None):
        try:
            if not user_id:
                user_id = g.user.id

            serializer = ProfileSerializer(data=data)

            if not serializer.is_valid():
                raise ValidationError(serializer.errors)

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
        except ValidationError as e:
            raise e
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            raise UnknownError()

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

    def get_details(self, teacher_id):
        return [
            {
                "id": item.id,
                "title": item.title,
                "dates": item.dates,
                "credits": item.credits
            } for item in self.teacher_detail_repository.find(teacher_id=teacher_id)
        ]

    def update_details(self, details, teacher_id):
        old_details = self.teacher_detail_repository.find(teacher_id=teacher_id)

        for item in old_details:
            if not any(el.get('id', None) == item.id for el in details):
                db.session.delete(item)

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

    def update_positions(self, positions, teacher_id):
        old_positions = self.teacher_positions_repository.find(teacher_id=teacher_id)

        for item in old_positions:
            if not any(el.get('id', None) == item.id for el in positions):
                db.session.delete(item)

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

    def update_courses(self, positions, teacher_id):
        old_data = self.teacher_course_repository.find(teacher_id=teacher_id)

        for item in old_data:
            if not any(el.get('id', None) == item.id for el in positions):
                db.session.delete(item)

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

    @staticmethod
    def update_teacher(model, data):
        if data.get('address', None):
            model.address = data['address']

        if data.get('phone', None):
            model.phone = data['phone']
