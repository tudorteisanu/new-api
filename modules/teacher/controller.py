from api import api
from modules.teacher.resource import TeacherResource
from modules.teacher.resource import TeacherOneResource
from modules.teacher.resource import TeacherListResource

resource = '/teachers'

api.add_resource(TeacherResource, resource)
api.add_resource(TeacherOneResource, f'{resource}/<model_id>')
api.add_resource(TeacherListResource, f'{resource}/list')
