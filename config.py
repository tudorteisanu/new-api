from datetime import timedelta
from os import environ

POSTGRES = {
    'user': 'aolxbrsq',
    'pw': 'j8U0Zcn_2IIHkD7Po283easg1fNJAx8m',
    'db': 'aolxbrsq',
    'host': 'queenie.db.elephantsql.com'
}


class FlaskConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s/%(db)s' % POSTGRES
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///app2.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'MY_SERCRET_KEY'

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_HEADER_TYPE = ""
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'it.worker995@gmail.com'
    MAIL_PASSWORD = 'Light231'


class Config(object):
    LANGUAGES = ['ro', 'ru', 'en']

    backendAddress = "http://localhost:5001"
    
    client_id = "292354651649-uj8lan8ni8r1ku31k2c4ko2hpbi08sq2.apps.googleusercontent.com"
    client_secret = "3AASA6vUb5xKgu567Wofgoxn"
    
    langs = ['ru', 'ro', 'en']
    
    MY_ADMINS = [
        "naker.official@gmail.com",
        "dmitrii.stoian@gmail.com",
        "gribinceaalina34@gmail.com"
    ]
        
    adminDefaultUsers = [
        "teisanutudort@gmail.com",
        "dmitrii.stoian@gmail.com",
        "gribinceaalina34@gmail.com",
        "test.mail.30.03.2019@gmail.com",
        "imspcmfbalti@gmail.com"
    ]

    seoDefaultUsers = [
        "teisanutudort@gmail.com",
        "dmitrii.stoian@gmail.com",
        "test.mail.30.03.2019@gmail.com",
        "info.kickrec@gmail.com",
        "info.kickrec.com@gmail.com"
    ]


class ProdConfig(Config):
    DEBUG = False
    backendAddress = environ.get('backendAddress')
    frontendAddress = 'https://'


class DevConfig(Config):
    DEBUG = True
    PORT = 5000
    HOST = "0.0.0.0"
    backendAddress = "http://0.0.0.0" + ":" + str(PORT)
    frontendAddress = 'https://'


# default config object
configType = DevConfig


class Common:
    # size from big to small
    images_with = [
        {"w": 390, "h": 390},
        {"w": 190, "h": 190}
    ]
    fileName = 'static/categories.json'
    fileNameAbout = 'static/categories-about.json'

    categoriesPath = 'static/'


class FirebaseConfig:
    projectId = 'forex-29cdf'
    fireBaseSendLink = "https://"
