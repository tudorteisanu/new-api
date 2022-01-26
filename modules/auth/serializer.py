from flask_simple_serializer.serializers import Serializer
from flask_simple_serializer import StringField, EmailField, validators


class LoginSerializer(Serializer):
    email = EmailField('Email Address', [validators.InputRequired(), validators.Length(min=4, max=25)])
    password = StringField('Password', [validators.InputRequired(), validators.Length(min=8, max=256)])
