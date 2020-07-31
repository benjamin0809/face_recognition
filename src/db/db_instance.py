
import redis


class Configuration(object):
    pool = any

    def __init__(self):
        try:
            self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
        except Exception as e:
            print(e)
    pass

