from src.services.serializer import serializer


class CreateUserSerializer(serializer.Base):
    email = serializer.String(min_length=2, max_length=150, required=True)
    name = serializer.String(min_length=2, max_length=150, required=True)
    role = serializer.String(min_length=2, max_length=150, required=True)

