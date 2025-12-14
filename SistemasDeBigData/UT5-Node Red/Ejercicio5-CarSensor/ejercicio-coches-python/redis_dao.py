import redis


class RedisDao:
    def __init__(self, hostname, port, database):
        self.__connection = redis.Redis(
            host=hostname,
            port=port,
            db=database,
            decode_responses=True
        )

    def set(self, key, value) -> any: # type: ignore
        return self.__connection.set(key, value)
    
    def increment(self, key):
        return self.__connection.incr(key)
    
    def get(self, key) -> any: # type: ignore
        return self.__connection.get(key)
    
    def close(self):
        self.__connection.close()

    """ TODO: crear los metodos necesarios para realizar las llamadas a Redis """
