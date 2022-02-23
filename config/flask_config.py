from datetime import timedelta
from os import environ

# POSTGRES = {
#     'user': environ.get('PG_USER'),
#     'pw': environ.get('PG_PASSWORD'),
#     'db': environ.get('PG_DB_NAME'),
#     'host': environ.get('PG_HOST')
# }
POSTGRES = {
    'user': 'yprnvaiz',
    'pw': '5vnB2YB_D3eGAhjMwQGEmp5TES8dFTJW',
    'db': 'yprnvaiz',
    'host': 'castor.db.elephantsql.com'
}


class FlaskConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s/%(db)s' % POSTGRES
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///app2.db'
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
    FRONTEND_ADDRESS = environ.get('FRONTEND_ADDRESS')
