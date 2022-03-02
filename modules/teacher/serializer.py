from flask_simple_serializer.serializers import Serializer
from flask_simple_serializer import StringField, EmailField, validators


class UserSerializer(Serializer):
    name = StringField('Name', [validators.InputRequired(), validators.Length(min=4, max=150)])


class CreateUserSerializer(Serializer):
    email = EmailField('email', [validators.InputRequired(), validators.Length(min=4, max=25)])
    password = StringField('password', [validators.InputRequired(), validators.Length(min=8, max=256)])
    name = StringField('name', [validators.InputRequired(), validators.Length(min=4, max=150)])


