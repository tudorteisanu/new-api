from apps.roles.models import Role
from marshmallow_sqlalchemy import ModelSchema


class RolesSchema(ModelSchema):
    class Meta:
        model = Role
