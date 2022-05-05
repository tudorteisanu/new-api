import logging
import os.path
from json import loads, dumps
from flask import request
from flask_restful import Resource

from src.exceptions.http import UnknownException
from src.exceptions.permissions import PermissionsException
from src.modules.roles.service import RolePermissionsRepository
from src.modules.roles.service import RoleRepository
from flask import g

role_permissions_repository = RolePermissionsRepository()
role_repository = RoleRepository()


class BaseResource(Resource):
    permissions = {}
    role_permissions_repository = role_permissions_repository
    role_repository = role_repository

    def __init__(self):
        self.permissions = {}
        self.role_permissions_repository = role_permissions_repository
        self.role_repository = role_repository

    def apply_permissions(self):
        try:
            endpoint = request.endpoint
            method = request.method

            if not g.user:
                raise PermissionsException(message='Not have enough permissions')

            if g.user.is_super_user:
                return True

            if not g.user.role_id:
                raise PermissionsException(message='Not have enough permissions')

            if not os.path.exists("config/permissions.json"):

                permission = self.role_permissions_repository.find_one(
                    endpoint=endpoint,
                    method=method,
                    role_id=g.user.role_id
                )

                if not permission:
                    raise PermissionsException(message='Not have enough permissions')

                self.generate_permissions_file()
            else:
                with open("config/permissions.json", 'r') as f:
                    data = loads(f.read())
                    items = data.get(g.user.role.alias, None)

                    if not items:
                        raise PermissionsException(message='Not have enough permissions')

                    if not items.get(endpoint, None):
                        raise PermissionsException(message='Not have enough permissions')

                    if method not in items[endpoint]:
                        raise PermissionsException(message='Not have enough permissions')

                    return True
        except Exception as e:
            logging.error(e)
            raise UnknownException()

    def generate_permissions_file(self):
        try:
            roles = self.role_repository.find()
            obj = {}

            for role in roles:
                obj[role.alias] = {}

                permissions = self.role_permissions_repository.find(role_id=g.user.role_id)

                for permission in permissions:

                    if not obj[role.alias].get(permission.endpoint, None):
                        obj[role.alias][permission.endpoint] = []

                    obj[role.alias][permission.endpoint].append(permission.method)

            with open("config/permissions.json", 'w') as f:
                f.write(dumps(obj))
        except Exception as e:
            raise e