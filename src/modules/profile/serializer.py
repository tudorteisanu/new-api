from src.services.serializer import serializer


class PositionsSerializer(serializer.Base):
    work_experience = serializer.Number(required=True)
    position_id = serializer.Exists(table='position', field='id', required=True)
    degree_id = serializer.Exists(table='degree', field='id', required=True)


class ProfileSerializer(serializer.Base):
    courses = serializer.List(required=True)
    details = serializer.List(required=True)
    positions = serializer.List(serializer=PositionsSerializer)

