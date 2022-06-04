from src.services.serializer import serializer


class EmailSerializer(serializer.Base):
    email = serializer.String(min_length=8, max_length=256, required=True)


class LoginSerializer(serializer.Base):
    email = serializer.String(min_length=8, max_length=256, required=True)
    password = serializer.String(required=True, min_length=8, max_length=256)


class RegisterSerializer(serializer.Base):
    name = serializer.String(min_length=2, max_length=256, required=True)
    email = serializer.String(min_length=8, max_length=256, required=True)
    password = serializer.String(required=True, min_length=8, max_length=256)


class ChangePasswordSerializer(serializer.Base):
    old_password = serializer.String(min_length=8, max_length=256, required=True)
    new_password = serializer.String(min_length=8, max_length=256, required=True)
    password_confirmation = serializer.String(min_length=8, max_length=256, required=True)


class ResetPasswordSerializer(serializer.Base):
    token = serializer.String(required=True)
    password = serializer.String(required=True, min_length=8, max_length=256)


class TokenSerializer(serializer.Base):
    token = serializer.String(required=True)


class ForgotPasswordSerializer(serializer.Base):
    email = serializer.String(required=True)
