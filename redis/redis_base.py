import redis

from ...conf import news_config


class Base(object):
    def __init__(self, *args, **kwargs):
        self._settings = news_config.settings
        self.redis = redis.Redis(self.host, *args, **kwargs)

    @property
    def host(self):
        return self._settings['REDIS_HOST']

    @property
    def filetr_key_md5(self):
        return self._settings['REDIS_FILTER_KEY']

    @property
    def sgp_hot_channel(self):
        return self._settings['SGP_HOT']

    @property
    def sgp_news_channel(self):
        return self._settings['SGP_NEWS']

    @property
    def sgp_hot_mq(self):
        return self._settings['SGP_HOT_MQ']

    @property
    def sgp_news_mq(self):
        return self._settings['SGP_NEWS_MQ']

    @property
    def proxy_ip_mq(self):
        return self._settings['SCRAPY_PROXY_IP_KEY']
