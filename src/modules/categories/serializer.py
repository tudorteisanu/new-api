from src.services.serializer import serializer


class CreateCategorySerializer(serializer.Base):
    name_ro = serializer.String(min_length=2, max_length=150, required=True)
    name_en = serializer.String(min_length=2, max_length=150, required=True)
    name_ru = serializer.String(min_length=2, max_length=150, required=True)
    user_id = serializer.Exists(table='user', field='id')

