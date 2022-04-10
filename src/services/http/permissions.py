import os
from json import loads, dumps
from src.app import db, app
from src.modules.permissions.models import Permission
from src.modules.roles.models import RolePermissions, Role


def load_perms(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = f.read()
            return loads(data)
    return None


def update_or_insert(perms):
    for item in perms:
        perm = Permission.query.filter_by(alias=item['alias']).first()

        if perm is not None:
            perm.name = item['name']

        else:
            perm = Permission(name=item['name'], alias=item['alias'])
            db.session.add(perm)


def add_all_perms():
    all_roles = Role.query.filter_by(alias='admin').all()
    for role in all_roles:
        permissions = Permission.query.all()

        for item in permissions:
            if not RolePermissions.query.filter_by(role_id=role.id, permission_id=item.id).first():
                db.session.add(RolePermissions(role_id=role.id, permission_id=item.id))


def save_permissions_to_file(global_perms=True):
    if global_perms:
        add_all_perms()

    roles = Role.query.all()
    perms = {}

    for role in roles:
        permissions_ids = [item.permission_id for item in role.permissions]
        perms[role.id] = [item.alias for item in Permission.query.filter(Permission.id.in_(permissions_ids))]

    with open("config/permissions.json", "w") as f:
        f.write(dumps(perms))

        print('-------- Permissions updated ----------')


def check_permissions(root_dir='src/modules'):
    try:
        for item in os.listdir(root_dir):
            if os.path.exists(f'{root_dir}/{item}/config/permissions.json'):
                perms = load_perms(f'{root_dir}/{item}/config/permissions.json')
                update_or_insert(perms)

        db.session.commit()
        save_permissions_to_file()
    except Exception as e:
        print(e)
        db.session.rollback()

