from src.services.serializer import serializer


class CreateGoodSerializer(serializer.Base):
    name_ro = serializer.String(min_length=2, max_length=150, required=True)
    name_en = serializer.String(min_length=2, max_length=150, required=True)
    name_ru = serializer.String(min_length=2, max_length=150, required=True)
    user_id = serializer.Exists(table='user', field='id')
    category_id = serializer.Exists(table='category', field='id')

