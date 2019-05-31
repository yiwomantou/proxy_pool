import redis
from random import choice

MAX_SCORE = 9999  # 最大值
PASS_SCORE = 100  # 及格线
MIN_SCORE = 0  # 移除线
INITIAL_SCORE = 10  # 初始线
REDIS_HOST = "120.78.212.251"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = "proxies"


class SaveModel(object):
    # 初始化
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    # 添加代理
    def add(self, proxy, score=INITIAL_SCORE):
        # REDIS_KEY = 集合中的名字, proxy = 集合中元素的名字
        if not self.db.zscore(REDIS_KEY, proxy):
            mapping = {
                proxy: score,
            }
            return self.db.zadd(REDIS_KEY, mapping=mapping)

    def random_get_proxy(self):
        result = self.db.zrangebyscore(REDIS_KEY, PASS_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, MIN_SCORE, PASS_SCORE)
            if len(result):
                return choice(result)
            else:
                return {"code": "0", "msg": "代理池为空"}

    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print("本次检测不合格，代理：{proxy}，当前分数为：{score}，减一".format(proxy=proxy, score=score))
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print("本次检测不合格，代理：{proxy}，当前分数为：{score}，移除".format(proxy=proxy, score=score))
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def set_score_max(self, proxy):
        print("本次检测合格，代理：{proxy}可用，设置为{score}".format(proxy=proxy, score=PASS_SCORE))
        return self.db.zadd(REDIS_KEY, proxy, PASS_SCORE)

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
