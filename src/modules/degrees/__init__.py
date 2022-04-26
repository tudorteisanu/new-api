from src.app import api
from .resource import DegreeResource, DegreeOneResource, DegreeListResource

resource = '/degrees'

api.add_resource(DegreeResource, resource)
api.add_resource(DegreeOneResource, f'{resource}/<model_id>')
api.add_resource(DegreeListResource, f'{resource}/list')
