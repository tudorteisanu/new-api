import os
from src.app import app
import argparse
from src.seeders import seed_db
from src.services.http.permissions import check_permissions


parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--perms", action="store_true")
parser.add_argument("--seed", action="store_true")
args = parser.parse_args()

if args.perms:
    check_permissions()

if args.seed:
    os.system('flask db upgrade')
    seed_db()
