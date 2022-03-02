from api import api
from modules.course.resource import CourseResource
from modules.course.resource import CourseOneResource
from modules.course.resource import CourseListResource

resource = '/courses'

api.add_resource(CourseResource, resource)
api.add_resource(CourseOneResource, f'{resource}/<model_id>')
api.add_resource(CourseListResource, f'{resource}/list')
