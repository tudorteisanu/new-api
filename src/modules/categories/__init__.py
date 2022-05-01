from src.app import api
from .models import Category
from .resource import CategoryResource
from .resource import CategoryOneResource
from .resource import CategoryListResource
from .resource import CategoriesPublicResource
from .resource import CategoriesPublicListResource

resource = '/categories'

api.add_resource(CategoryResource, resource)
api.add_resource(CategoryOneResource, f'{resource}/<model_id>')
api.add_resource(CategoryListResource, f'{resource}/list')
api.add_resource(CategoriesPublicResource, f'{resource}/public')
api.add_resource(CategoriesPublicListResource, f'{resource}/public/list')
