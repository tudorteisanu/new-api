from src.services.serializer import serializer


class CreateTeacherSerializer(serializer.Base):
    first_name = serializer.String(min_length=2, max_length=150, required=True)
    last_name = serializer.String(min_length=2, max_length=150, required=True)
    email = serializer.Email(required=True)
    password = serializer.String(min_length=8, max_length=255, required=True)
