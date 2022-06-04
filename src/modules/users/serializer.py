from src.services.serializer import serializer


class CreateUserSerializer(serializer.Base):
    email = serializer.Email(required=True)
    name = serializer.String(min_length=2, max_length=150, required=True)
    password = serializer.String(min_length=8, max_length=150, required=True)
    role_id = serializer.Exists(required=True, table='role', field='id')

