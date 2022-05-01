import os
from json import loads, dumps
from src.app import db
from src.modules.permissions.repository import PermissionRepository
from src.modules.roles.models import RolePermissions
from src.modules.roles.models import Role


class UpdatePermissions:
    def __init__(self):
        self.permission_repository = PermissionRepository()

    def load_perms(path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = f.read()
                return loads(data)
        return None


    def update_or_insert(perms):
        for item in perms:
            perm = PermissionRepository.find_one(alias=item['alias'])

            if perm is not None:
                perm.name = item['name']

            else:
                perm = Permission(name=item['name'], alias=item['alias'])
                db.session.add(perm)

    def add_all_perms(self):
        all_roles = Role.query.filter_by(alias='admin').all()

        for role in all_roles:
            permissions = self.permission_repository.find()

            for item in permissions:
                if not RolePermissions.query.filter_by(role_id=role.id, permission_id=item.id).first():
                    db.session.add(RolePermissions(role_id=role.id, permission_id=item.id))

    def save_permissions_to_file(self, global_perms=True):
        if global_perms:
            self.add_all_perms()

        roles = Role.query.all()
        perms = {}

        for role in roles:
            permissions_ids = [item.permission_id for item in role.permissions]
            perms[role.alias] = [item.alias for item in self.permission_repository.get_by_ids(permissions_ids)]

        with open("config/permissions.json", "w") as f:
            f.write(dumps(perms))

            print('-------- Permissions updated ----------')

    def check_permissions(self, root_dir='src/modules'):
        try:
            for item in os.listdir(root_dir):
                if os.path.exists(f'{root_dir}/{item}/config/permissions.json'):
                    perms = self.load_perms(f'{root_dir}/{item}/config/permissions.json')
                    self.update_or_insert(perms)

            db.session.commit()
            self.save_permissions_to_file()
        except Exception as e:
            print(e)
            db.session.rollback()

