from datetime import timedelta
from os import environ

from dotenv import load_dotenv

load_dotenv('.env')

POSTGRES = {
    'user': environ.get('PG_USER'),
    'pw': environ.get('PG_PASSWORD'),
    'db': environ.get('PG_DB_NAME'),
    'host': environ.get('PG_HOST'),
    'port': environ.get('PG_PORT', 5432),
}


class FlaskConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'MY_SECRET_KEY'

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_HEADER_TYPE = ""

    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEBUG = False
    SECURITY_PASSWORD_SALT = 'some_salt'

    DEBUG = True
    PORT = environ.get('PORT')
    HOST = environ.get('HOST')

    BACKEND_ADDRESS = environ.get('BACKEND_ADDRESS')
    STATIC_PATH = environ.get('STATIC_PATH')
    FRONTEND_ADDRESS = environ.get('FRONTEND_ADDRESS')
    PERMISSIONS = "config/permissions.json"
