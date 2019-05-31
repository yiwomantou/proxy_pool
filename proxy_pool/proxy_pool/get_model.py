from proxy_pool import crawl_model
from proxy_pool import save_model

POOL_UPPER_THRESHOLD = 10000  # 代理池最大条数


class Getter(object):
    def __init__(self):
        self.redis = save_model.SaveModel()
        self.crawler = crawl_model.Crawler()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print("获取器开始执行")
        if not self.is_over_threshold():
            print(self.crawler.__CrawlFunc__)
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = eval("self.crawler.{}()".format(callback))
                for proxy in proxies:
                    print(proxy)
                    self.redis.add(proxy)


if __name__ == "__main__":
    getter = Getter()
    getter.run()
