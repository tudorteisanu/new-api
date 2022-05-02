from src.app import db
from .models import Teacher
from .models import TeacherPositions
from .models import TeacherCourse
from .models import TeacherDetails
from src.services.utils.repository import Repository


class TeacherRepository(Teacher, Repository):
    @staticmethod
    def create(**kwargs):
        model = Teacher(**kwargs)
        db.session.add(model)
        db.session.flush()
        return model


class TeacherCourseRepository(TeacherCourse, Repository):
    @staticmethod
    def create(**kwargs):
        model = TeacherCourse(**kwargs)
        db.session.add(model)
        db.session.flush()
        return model


class TeacherDetailsRepository(TeacherDetails, Repository):
    @staticmethod
    def create(**kwargs):
        model = TeacherDetails(**kwargs)
        db.session.add(model)
        db.session.flush()
        return model


class TeacherPositionsRepository(TeacherPositions, Repository):
    @staticmethod
    def create(**kwargs):
        model = TeacherPositions(**kwargs)
        db.session.add(model)
        db.session.flush()
        return model
