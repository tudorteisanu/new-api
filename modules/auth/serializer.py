from flask_simple_serializer.serializers import Serializer
from flask_simple_serializer import StringField, EmailField, validators


class LoginSerializer(Serializer):
    email = EmailField('Email Address', [validators.InputRequired(), validators.Length(min=4, max=25)])
    password = StringField('Password', [validators.InputRequired(), validators.Length(min=8, max=256)])


class RegisterSerializer(Serializer):
    email = EmailField('Email Address', [validators.InputRequired(), validators.Length(min=4, max=25)])
    password = StringField('Password', [validators.InputRequired(), validators.Length(min=8, max=256)])
    name = StringField('name', [validators.InputRequired(), validators.Length(min=2, max=150)])


class ChangePasswordSerializer(Serializer):
    old_password = StringField('old_password', [validators.InputRequired(), validators.Length(min=8, max=256)])
    new_password = StringField('new_password', [validators.InputRequired(), validators.Length(min=8, max=256)])
    password_confirmation = StringField('password_confirmation',
                                        [validators.InputRequired(), validators.Length(min=8, max=256)])
