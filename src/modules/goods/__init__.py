from src.app import api
from .models import Good
from src.modules.goods.resource import GoodsResource, GoodsOneResource, GoodsListResource
from src.modules.goods.resource import GoodsPublicListResource, GoodsPublicResource, GoodsOnePublicListResource

resource = '/goods'

api.add_resource(GoodsResource, resource)
api.add_resource(GoodsOneResource, f'{resource}/<model_id>')
api.add_resource(GoodsListResource, f'{resource}/list')
api.add_resource(GoodsPublicListResource, f'{resource}/public/list')
api.add_resource(GoodsPublicResource, f'{resource}/<int:category_id>/public')
api.add_resource(GoodsOnePublicListResource, f'{resource}/public/<int:model_id>/show')
