from os.path import abspath as _abs
from redis import (AuthenticationError,
                   BusyLoadingError,
                   ConnectionError,
                   DataError,
                   InvalidResponse,
                   ReadOnlyError,
                   RedisError,
                   ResponseError,
                   TimeoutError,
                   WatchError
                   )

from . import logger
from .base import Base


class RedisCached(Base):
    def set(self, default_key=None, *value):
        """
        add url or title value of news to set
        :param value: string, md5 value
        :param default_key: None|string, set key to redis
        """
        set_key = default_key or self.scrapy_filter_key

        try:
            self.redis.sadd(set_key, *value)
        except (AuthenticationError, BusyLoadingError, ConnectionError, DataError, InvalidResponse,
                ReadOnlyError, RedisError, ResponseError, TimeoutError, WatchError) as e:
            logger.info('Set value to Redis error: key <{}>, type <{}>, msg <{}>, file <{}>'.format(
                set_key, e.__class__, e, _abs(__file__)))

    def get(self, default_key=None):
        """
        get all members from set of specified key
        :param default_key: None|string, set key to redis
        """
        set_key = default_key or self.scrapy_filter_key

        try:
            return self.redis.smembers(set_key)
        except (AuthenticationError, BusyLoadingError, ConnectionError, DataError, InvalidResponse,
                ReadOnlyError, RedisError, ResponseError, TimeoutError, WatchError) as e:
            logger.info('Get value from Redis error: key <{}>, type <{}>, msg <{}>, file <{}>'.format(
                set_key, e.__class__, e, _abs(__file__)))
        return set()

    def rem(self, default_key=None, *value):
        set_key = default_key or self.scrapy_filter_key

        try:
            self.redis.srem(set_key, *value)
        except (AuthenticationError, BusyLoadingError, ConnectionError, DataError, InvalidResponse,
                ReadOnlyError, RedisError, ResponseError, TimeoutError, WatchError) as e:
            logger.info('Remove value from Redis error: key <{}>, type <{}>, msg <{}>, file <{}>'.format(
                set_key, e.__class__, e, _abs(__file__)))
