from src.app import api
from src.modules.teacher.resource import TeacherResource, TeacherOneResource, TeacherListResource

resource = '/teachers'

api.add_resource(TeacherResource, resource)
api.add_resource(TeacherOneResource, f'{resource}/<model_id>')
api.add_resource(TeacherListResource, f'{resource}/list')
