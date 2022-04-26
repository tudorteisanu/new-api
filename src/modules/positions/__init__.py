from src.app import api
from .resource import PositionResource
from .resource import PositionOneResource
from .resource import PositionListResource

resource = '/positions'

api.add_resource(PositionResource, resource)
api.add_resource(PositionOneResource, f'{resource}/<model_id>')
api.add_resource(PositionListResource, f'{resource}/list')
