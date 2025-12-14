import os

from dao.redis_dao import RedisDao
from dao.mongo_dao import MongoDao
from dao.postgres_dao import PostgresDao

def init():
    global redis_dao
    redis_dao = RedisDao(
        hostname=os.getenv('REDIS_HOSTNAME'),
        port=os.getenv('REDIS_PORT'),
        database=os.getenv('REDIS_DATABASE')
    )

    global mongo_dao
    mongo_dao = MongoDao(
        hostname=os.getenv('MONGO_HOSTNAME'),
        port=os.getenv('MONGO_PORT'),
        database=os.getenv('MONGO_DATABASE'),
        user=os.getenv('MONGO_USER'),
        password=os.getenv('MONGO_PASSWORD')
    )

    global postgres_dao
    postgres_dao = PostgresDao(
        hostname=os.getenv('POSTGRES_HOSTNAME'),
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('POSTGRES_DATABASE'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )