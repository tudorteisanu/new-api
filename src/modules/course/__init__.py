from src.app import api
from .resource import CourseResource, CourseOneResource, CourseListResource
from .models import Course

resource = '/courses'

api.add_resource(CourseResource, resource)
api.add_resource(CourseOneResource, f'{resource}/<model_id>')
api.add_resource(CourseListResource, f'{resource}/list')
