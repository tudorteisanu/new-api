from src.app import api
from src.modules.position.resource import PositionResource, PositionOneResource, PositionListResource

resource = '/positions'

api.add_resource(PositionResource, resource)
api.add_resource(PositionOneResource, f'{resource}/<model_id>')
api.add_resource(PositionListResource, f'{resource}/list')
