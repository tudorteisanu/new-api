import logging
from src.app import db

from src.services.utils.repository import Repository
from src.exceptions.database import SqlException

from .models import Teacher
from .models import TeacherPositions
from .models import TeacherCourse
from .models import TeacherDetails


class TeacherRepository(Teacher, Repository):
    @staticmethod
    def create(**kwargs):
        try:
            model = Teacher(**kwargs)
            db.session.add(model)
            db.session.flush()
            return model
        except Exception as e:
            logging.error(e)
            raise SqlException(e)


class TeacherCourseRepository(TeacherCourse, Repository):
    @staticmethod
    def create(**kwargs):
        try:
            model = TeacherCourse(**kwargs)
            db.session.add(model)
            db.session.flush()
            return model
        except Exception as e:
            logging.error(e)
            raise SqlException(e)


class TeacherDetailsRepository(TeacherDetails, Repository):
    @staticmethod
    def create(**kwargs):
        try:
            model = TeacherDetails(**kwargs)
            db.session.add(model)
            db.session.flush()
            return model
        except Exception as e:
            logging.error(e)
            raise SqlException(e)


class TeacherPositionsRepository(TeacherPositions, Repository):
    @staticmethod
    def create(**kwargs):
        try:
            model = TeacherPositions(**kwargs)
            db.session.add(model)
            db.session.flush()
            return model
        except Exception as e:
            logging.error(e)
            raise SqlException(e)
