from src.services.serializer import serializer


class CreateDegreeSerializer(serializer.Base):
    name = serializer.String(min_length=2, max_length=255)

