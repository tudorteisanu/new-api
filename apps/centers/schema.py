from settings import ma
from apps.centers.models import Center


class CenterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Center
