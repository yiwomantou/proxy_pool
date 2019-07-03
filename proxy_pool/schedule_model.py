import time
from multiprocessing import Process
from proxy_pool.interface_model import app
from proxy_pool.crawl_model import Getter
from proxy_pool.check_model import Tester
from proxy_pool.setting import logger

TESTER_CYCLE = 60 * 5
GETTER_CYCLE = 60 * 60 * 12
TESTER_ENABLE = True
GETTER_ENABLE = True
API_ENABLE = True
API_HOST = '0.0.0.0'
API_PORT = '8080'


class Schedule(object):
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle: 间隔时间
        :return: None
        """
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        :param cycle: 周期
        :return: None
        """
        getter = Getter()
        while True:
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启api
        :return: None
        """
        logger.info('接口开启')
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        logger.info('代理池开始运行')
        if TESTER_ENABLE:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLE:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLE:
            api_process = Process(target=self.schedule_api)
            api_process.start()


if __name__ == '__main__':
    schedule = Schedule()
    schedule.run()
