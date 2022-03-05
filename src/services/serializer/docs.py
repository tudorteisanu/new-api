from src import serializer


class Names(serializer.Base):
    alias = serializer.String(required=True, min_length=2, max_length=7)
    alias2 = serializer.String(required=True, min_length=2, max_length=7)
    alias3 = serializer.String(required=True, min_length=2, max_length=7)


class NamesSerializer(serializer.Base):
    l2 = serializer.String(required=True, min_length=2, max_length=7)
    monkey = serializer.List(serializer=Names, required=True)


class RoleSerializer(serializer.Base):
    alias = serializer.String(required=True, min_length=2, max_length=7)
    name = serializer.List(serializer=NamesSerializer, required=True)


class LoginSerializer(serializer.Base):
    email = serializer.String(min_length=2, max_length=7)
    password = serializer.String(min_length=8, max_length=256)
    role = RoleSerializer
