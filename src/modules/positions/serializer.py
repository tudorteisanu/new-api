from src.services.serializer import serializer


class CreatePositionSerializer(serializer.Base):
    name = serializer.String(min_length=2, max_length=255)

