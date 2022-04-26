from src.services.serializer import serializer


class CreateNotificationSerializer(serializer.Base):
    description = serializer.String(min_length=10, max_length=256)
    title = serializer.String(min_length=10, max_length=256)

