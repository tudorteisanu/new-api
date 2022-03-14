from src.services.serializer import serializer


class CreateUserSerializer(serializer.Base):
    email = serializer.Email(required=True)
    name = serializer.String(min_length=2, max_length=150, required=True)
    roles = serializer.List(required=True)

