import os

from src.app import app, FlaskConfig
from src.services.logs import init_logging
from src.services.http.permissions import check_permissions
import argparse

if FlaskConfig.PRODUCTION:
    init_logging(app)

parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--perms", action="store_true")
parser.add_argument("--seed", action="store_true")
args = parser.parse_args()

if args.perms:
    check_permissions()

if args.seed:
    os.system('flask db upgrade')
    os.system('python seeder.py')

if not FlaskConfig.PRODUCTION:
    if __name__ == '__main__':
        app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
