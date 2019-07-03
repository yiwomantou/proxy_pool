import asyncio
import time
import aiohttp
from proxy_pool.save_model import SaveModel
from proxy_pool.setting import logger

VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100


class Tester(object):
    def __init__(self):
        self.redis = SaveModel()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 代理
        :return: None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                logger.info('正在测试' + proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                    else:
                        self.redis.decrease(proxy)
                        logger.info('请求的响应码不合理' + proxy)
            except:
                self.redis.decrease(proxy)
                logger.info('代理请求失败' + proxy)

    def run(self):
        """
        测试主函数
        :return: None
        """
        logger.info('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i: i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except:
            logger.info('测试器发生错误')


if __name__ == '__main__':
    test = Tester()
    test.run()
