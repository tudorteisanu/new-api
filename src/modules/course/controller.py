from src.app import api
from src.modules.course.resource import CourseResource, CourseOneResource, CourseListResource

resource = '/courses'

api.add_resource(CourseResource, resource)
api.add_resource(CourseOneResource, f'{resource}/<model_id>')
api.add_resource(CourseListResource, f'{resource}/list')
