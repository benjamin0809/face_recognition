import redis

from .db_instance import Configuration
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)


class RedisService(object):

    @staticmethod
    def redis_set(key_name, bytes):
        # 连数据库
        # 录入人名-对应特征向量
        r.set(key_name, bytes)

    @staticmethod
    def redis_get(name):
        # 连数据库
        faces = r.get(name)
        return faces

    @staticmethod
    def redis_get_all():
        # 连数据库
        names = r.keys()
        faces = r.mget(names)
        return faces

    @staticmethod
    def redis_get_names():
        names = r.keys()
        return names

    @staticmethod
    def redis_clear_key(key_name):
        r.delete(key_name)
        return 1

    @staticmethod
    def redis_clear_all():
        names = r.keys()
        r.delete()
        return names

    @staticmethod
    def get_pool():
        return Configuration.pool
