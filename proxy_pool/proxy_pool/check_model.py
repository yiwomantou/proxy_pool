import time
import asyncio
import aiohttp
from proxy_pool import save_model

VALID_STATUS_CODES = [200]  # 请求成功状态
TEST_URL = "https://www.baidu.com"  # 测试的url
BATCH_TEST_SIZE = 100  # 异步的数量


class Tester(object):
    def __init__(self):
        self.redis = save_model.SaveModel()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf-8")
                real_proxy = "http://" + proxy
                print("正在测试：{}".format(proxy))
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.set_score_max(proxy)
                        print("代理可用{}".format(proxy))
                    else:
                        self.redis.decrease(proxy)
                        print("请求响应码不合法{}".format(proxy))
            except:
                self.redis.decrease(proxy)
                print("代理请求失败{}".format(proxy))

    def run(self):
        print("开始检测代理")
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print("测试器发生错误", e.args)


if __name__ == "__main__":
    tester = Tester()
    tester.run()
