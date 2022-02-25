from app import api
from modules.position.resource import PositionResource
from modules.position.resource import PositionOneResource
from modules.position.resource import PositionListResource

resource = '/positions'

api.add_resource(PositionResource, resource)
api.add_resource(PositionOneResource, f'{resource}/<model_id>')
api.add_resource(PositionListResource, f'{resource}/list')
