import os
from src.app import app, db
import argparse
from src.seeders import seed_db
from src.services.permissions import permissions_service


parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--perms", action="store_true")
parser.add_argument("--seed", action="store_true")
parser.add_argument("--run", action="store_true")
parser.add_argument("--migrate", action="store_true")
parser.add_argument("--drop", action="store_true")
args = parser.parse_args()


def remove_files_from_dir(dir, root_dir='static'):
    for root, dirs, files in os.walk(f'static/{dir}'):
        for file in files:
            os.remove(os.path.join(root, file))


def remove_files():
    dirs = ['categories', 'goods']

    for item in dirs:
        remove_files_from_dir(item)


if args.drop:
    db.session.commit()
    db.drop_all()
    db.create_all()
    db.session.commit()

if args.migrate:
    os.system('flask db upgrade')

if args.seed:
    remove_files()
    seed_db()

if args.perms:
    permissions_service.check_permissions()

if args.run:
    app.run()



