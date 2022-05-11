import os
from src.app import app, db
import argparse
from src.seeders import seed_db
from src.modules.roles.service import RolePermissionsRepository
from src.modules.roles.service import RoleRepository

roles_permissions_repository = RolePermissionsRepository()
roles_repository = RoleRepository()


def add_all_perms():
    role = roles_repository.find_one(alias='admin')

    for rule in app.url_map.iter_rules():
        for method in rule.methods:
            if method not in ['HEAD', 'OPTIONS']:
                if not roles_permissions_repository.find_one(endpoint=rule.endpoint, method=method, role_id=role.id):
                    roles_permissions_repository.create(endpoint=rule.endpoint, method=method, role_id=role.id)
                    db.session.commit()
    return True


parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--perms", action="store_true")
parser.add_argument("--seed", action="store_true")
parser.add_argument("--migrate", action="store_true")
parser.add_argument("--drop", action="store_true")
args = parser.parse_args()


if args.drop:
    db.session.commit()
    db.drop_all()
    db.session.commit()


if args.migrate:
    os.system('flask db upgrade')

if args.seed:
    seed_db()

if args.perms:
    add_all_perms()



