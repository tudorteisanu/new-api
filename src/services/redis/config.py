from redis import Redis
from src.app import FlaskConfig

redis = Redis(
    host=FlaskConfig.REDIS_HOST,
    port=FlaskConfig.REDIS_PORT,
    password=FlaskConfig.REDIS_PASSWORD
)
