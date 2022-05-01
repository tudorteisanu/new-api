from .redis import RedisService

redis_service = RedisService()


class RedisKeys:
    positions_list = 'positions_list'
    degrees_list = 'degrees_list'
    teachers_list = 'teachers_list'
