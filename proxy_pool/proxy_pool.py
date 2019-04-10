"""
代理池
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import time


class ProxyPool(object):
    url = []
    count = 0
    proxies = []

    # 初始化参数
    def __init__(self, num, page):
        self.thread_num = num
        self.page = page

    # 拼接url
    def get_url(self):
        for i in range(self.page):
            self.url.append("https://www.xicidaili.com/nn/" + str(i + 1))

    # 爬取代理ip
    def get_proxy(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        while len(self.url) != 0:
            url = self.url.pop()
            r = requests.get(url=url, headers=headers)
            html = BeautifulSoup(r.text, "lxml")
            trs = html.select_one("#ip_list").select("tr")
            for tr in trs[1:]:
                proxy = {}
                tds = tr.select("td")
                protocol = tds[5].get_text().lower()
                if protocol == "https":
                    ip = tds[1].get_text()
                    port = tds[2].get_text()
                    proxy[protocol] = ip + ":" + port
                    self.proxies.append(proxy)

    # 验证代理是否可用
    def verify_proxy(self):
        while len(self.proxies) != 0:
            proxy = self.proxies.pop()
            try:
                r = requests.get(url="https://www.baidu.com", proxies=proxy, timeout=5)
                if r.status_code == 200:
                    with open(file="proxy.txt", mode="a", encoding="utf-8") as f:
                        f.write(str(proxy) + "\n")
                print("还有%s需要执行..." % (self.count - 1,))
                self.count = self.count - 1
            except:
                print("还有%s需要执行..." % (self.count - 1,))
                self.count = self.count - 1

    # 开启多线程
    def start_work(self):
        self.get_url()
        thread_list = []
        for i in range(5):
            thread = threading.Thread(target=self.get_proxy)
            thread.start()
            thread_list.append(thread)
            time.sleep(1)

        # 让主线程等待，等待所有子线程执行结束，再向下执行代码
        for thread in thread_list:
            thread.join()

        self.count = len(self.proxies)
        print("一共有%s条代理..." % self.count)
        print("代理爬取完毕，现在开始验证...")

        thread_list = []
        for i in range(self.thread_num):
            thread = threading.Thread(target=self.verify_proxy)
            thread.start()
            thread_list.append(thread)

        # 让主线程等待，等待所有子线程执行结束，再向下执行代码
        for thread in thread_list:
            thread.join()
        with open(file="proxy.txt", mode="a", encoding="utf-8") as f:
            f.write("----------------------------------------" + str(datetime.now()) + "\n")


if __name__ == "__main__":
    proxy_pool = ProxyPool(10, 10)
    proxy_pool.start_work()
