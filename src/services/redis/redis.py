import logging

from src.app import redis
from json import dumps, loads


class RedisService:
    def __init__(self):
        self.redis = redis

    def get(self, key):
        try:
            if self.redis.get(key):
                return loads(self.redis.get(key))
            return None
        except Exception as e:
            logging.error(e)
            return None

    def set(self, key, data):
        try:
            self.redis.set(key, dumps(data))
        except Exception as e:
            logging.error(e)
            return None
