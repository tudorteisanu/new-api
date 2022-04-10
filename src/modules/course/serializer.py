from src.services.serializer import serializer


class CreateCourseSerializer(serializer.Base):
    credits = serializer.Number(min_value=0, max_value=256)
    description = serializer.String(min_length=10, max_length=256)
    name = serializer.String(min_length=10, max_length=256)
    start_date = serializer.String(required=True)
    end_date = serializer.String(required=True)
    teacher_id = serializer.Number(required=True)

