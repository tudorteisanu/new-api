from settings import ma
from apps.products.models import Products         


class ProductsSchema(ma.SQLAlchemyAutoSchema):
         
	class Meta:         
		model = Products