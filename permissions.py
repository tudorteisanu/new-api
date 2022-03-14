import os
from json import loads
from src.app import db
from src.modules.permissions.models import Permission
from src.modules.roles.models import Role, RolePermissions
from src.modules.roles.service import save_permissions_to_file


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
    role = Role.query.filter_by(alias='admin').first()

    if role:
        permissions = Permission.query.all()

        for item in permissions:
            if not RolePermissions.query.filter_by(role_id=role.id, permission_id=item.id).first():
                db.session.add(RolePermissions(role_id=role.id, permission_id=item.id))


def check_permissions(root_dir='src/modules'):
    try:
        for item in os.listdir(root_dir):
            if os.path.exists(f'{root_dir}/{item}/config/permissions.json'):
                perms = load_perms(f'{root_dir}/{item}/config/permissions.json')
                update_or_insert(perms)
                print(f'<{item}> permissions updated')
                print('-'*200)

        add_all_perms()
        db.session.commit()
        save_permissions_to_file()
    except Exception as e:
        print(e)
        db.session.rollback()


if __name__ == '__main__':
    check_permissions()
