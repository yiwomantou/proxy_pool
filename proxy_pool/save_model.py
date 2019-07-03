import redis
from random import choice
from proxy_pool.setting import logger

# 代理分数设置
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

# redis信息配置
REDIS_HOST = '120.78.212.251'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'


class SaveModel(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: redis 的地址
        :param port: redis 的端口
        :param password: redis 的密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置初始分数
        :param proxy: 需要添加的代理
        :param score: 初始分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数的代理，如果最高分数不存在，则按照排名获取，否则返回None
        :return: 有效代理或者None
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                return None

    def decrease(self, proxy):
        """
        代理分数减一或者移除代理
        :param proxy: 代理
        :return: 代理减一或移除
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            logger.info('代理 {}，当前分数{}，分数减一'.format(proxy, score))
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            logger.info('代理 {}，当前分数{}，移除'.format(proxy, score))
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy: 代理
        :return: Boolean
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理的分数设置为 MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        logger.info('代理 {} 可用，设置为{}'.format(proxy, MAX_SCORE))
        return self.db.zadd(REDIS_KEY, {MAX_SCORE: proxy})

    def count(self):
        """
        获取代理数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)


if __name__ == '__main__':
    db = SaveModel()
    print(db.all())
