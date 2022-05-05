from celery import Celery

from src.app import FlaskConfig

REDIS_CONFIG = {
    "host": FlaskConfig.REDIS_HOST,
    "port": FlaskConfig.REDIS_PORT,
    "password": FlaskConfig.REDIS_PASSWORD
}

RABBITMQ_CONFIG = {
    "host": FlaskConfig.RABBITMQ_HOST,
    "port": FlaskConfig.RABBITMQ_PORT,
    "user": FlaskConfig.RABBITMQ_USER,
    "password": FlaskConfig.RABBITMQ_PASSWORD
}

REDIS_URI = 'redis://%(host)s:%(port)s' % REDIS_CONFIG
RABBITMQ_URI = 'amqp://%(user)s:%(password)s@%(host)s:%(port)s//' % RABBITMQ_CONFIG

celery = Celery('tasks', backend=REDIS_URI, broker=RABBITMQ_URI)
