from flask import request
from flask import jsonify
from sqlalchemy import exc
import logging

from api import db

from modules.course.models import Course
from modules.course.repository import CourseRepository

from services.http.errors import InternalServerError
from services.http.errors import NotFound
from services.http.errors import UnprocessableEntity
from services.http.errors import Success


class CourseService:
    def __init__(self):
        self.repository = CourseRepository()

    def find(self):
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "start_date", "text": 'Start date'},
            {"value": "end_date", "text": 'End date'},
            {"value": "teacher_id", "text": 'Teacher ID'},
            {"value": "credits", "text": 'Credits'},
        ]

        params = request.args

        items = self.repository \
            .paginate(int(params.get('page', 1)), per_page=int(params.get('per_page', 20)))

        resp = {
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "start_date": item.start_date,
                    "end_date": item.end_date,
                    "credits": item.credits,
                    "teacher_id": item.teacher_id,
                } for item in items.items],
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }

        return jsonify(resp)

    def create(self):
        try:
            data = request.json or request.form
            model = Course(
                name=data['name'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                teacher_id=data['teacher_id'],
                credits=data['credits']
            )
            self.repository.create(model)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def find_one(self, model_id):
        try:
            model = self.repository.find_one_or_fail(model_id)

            if not model:
                return NotFound(message='Course not found')

            return {
                    "id": model.id,
                    "name": model.name,
                    "start_date": model.start_date,
                    "end_date": model.end_date,
                    "credits": model.credits,
                    "teacher_id": model.teacher_id,
                }
        except Exception as e:
            logging.error(e)
            return InternalServerError()

    def edit(self, user_id):
        try:
            data = request.json
            model = self.repository.get(user_id)

            if not model:
                return NotFound()

            self.repository.update(model, data)
            db.session.commit()
            return Success()
        except exc.IntegrityError as e:
            db.session.rollback()
            logging.error(e)
            return UnprocessableEntity(message=f"{e.orig.diag.message_detail}")
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return InternalServerError()

    def delete(self, model_id):
        try:
            model = self.repository.get(model_id)

            if not model:
                return NotFound()

            self.repository.remove(model)
            db.session.commit()
            return Success()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return InternalServerError()

    def get_list(self):
        try:
            return self.repository.list()
        except Exception as e:
            logging.error(e)
            return InternalServerError()
