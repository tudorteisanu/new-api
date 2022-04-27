from src.services.serializer import serializer


class ProfileSerializer(serializer.Base):
    work_experience = serializer.Number(required=True)
    courses = serializer.List(required=True)
    details = serializer.List(required=True)
    position_id = serializer.Exists(table='position', field='id', required=True)
    degree_id = serializer.Exists(table='degree', field='id', required=True)

