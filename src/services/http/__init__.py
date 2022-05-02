from json import loads
from flask import request
from flask_restful import Resource

from src.exceptions.permissions import PermissionsExceptions
from flask import g


class BaseResource(Resource):
    permissions = {}

    def __init__(self):
        self.permissions = {}

    def apply_permissions(self):
        with open("config/permissions.json", 'r') as f:
            data = loads(f.read())

            if not g.user or not g.user.role_id:
                raise PermissionsExceptions(message='Not have enough permissions')

            if self.permissions.get(request.method, None) is None:
                raise PermissionsExceptions(message='Not have enough permissions')

            for item in self.permissions[request.method]:
                if not data.get(g.user.role.alias, None):
                    raise PermissionsExceptions(message='Not have enough permissions')

                if item in data[g.user.role.alias]:
                    return True

            raise PermissionsExceptions(message='Not have enough permissions')

