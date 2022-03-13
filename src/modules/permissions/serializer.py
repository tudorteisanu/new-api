from src.services.serializer import serializer


class CreatePermissionSerializer(serializer.Base):
    name = serializer.String(min_length=2, max_length=150, required=True)
    alias = serializer.String(min_length=2, max_length=150, required=True)

