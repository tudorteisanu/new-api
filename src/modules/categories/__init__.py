from src.app import api
from .models import Category
from src.modules.categories.resource import CategoryResource, CategoryOneResource, CategoryListResource

resource = '/categories'

api.add_resource(CategoryResource, resource)
api.add_resource(CategoryOneResource, f'{resource}/<model_id>')
api.add_resource(CategoryListResource, f'{resource}/list')
