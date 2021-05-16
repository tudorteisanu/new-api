from apps.clients.models import Client
from marshmallow_sqlalchemy import ModelSchema


class ClientSchema(ModelSchema):
    class Meta:
        model = Client
