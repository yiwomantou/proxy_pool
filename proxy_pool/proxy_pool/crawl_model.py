import json
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    # def get_proxies(self, callback):
    #     proxy = eval("self.{}".format(callback))
    #     print("成功获取到代理", proxy)
    #     return proxy

    def crawl_xici(self):
        print("爬取西刺代理")
        for x in range(10):
            yield ":".join(["120.78.212", str(x)])

    def crawl_360(self):
        print("爬取360代理")
        for x in range(10):
            yield ":".join(["120.78.212.251", str(100 - x)])
