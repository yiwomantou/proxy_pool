import time
from pyquery import PyQuery as pq
import requests
from proxy_pool.save_model import SaveModel
from proxy_pool.setting import logger

POOL_UPPER_THRESHOLD = 10000


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            logger.info('成功获取代理{}'.format(proxy))
            proxies.append(proxy)
        return proxies

    def crawl_xici(self, page_count=10):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36,'
        }
        start_url = 'https://www.xicidaili.com/nn/'
        urls = [start_url + str(i + 1) for i in range(page_count)]
        for url in urls:
            logger.info('Crawling' + url)
            r = requests.get(url=url, headers=headers)
            doc = pq(r.text)
            items = doc('tr').items()
            for index, item in enumerate(items):
                if index == 0:
                    continue
                ip = item('td:nth-child(2)').text()
                port = item('td:nth-child(3)').text()
                yield ':'.join([ip, port])
            time.sleep(5)


class Getter(object):
    def __init__(self):
        self.redis = SaveModel()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否超过了代理池限制
        :return: True 或者 False
        """
        if self.redis.count() > POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        logger.info('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl_xici()
