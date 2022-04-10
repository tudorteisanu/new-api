from src.services.serializer import serializer


class CreateTeacherSerializer(serializer.Base):
    first_name = serializer.String(min_length=2, max_length=150, required=True)
    last_name = serializer.String(min_length=2, max_length=150, required=True)
    address = serializer.String(min_length=2, max_length=150, required=True)
    user_id = serializer.Exists(required=True, table='user', field='id')

