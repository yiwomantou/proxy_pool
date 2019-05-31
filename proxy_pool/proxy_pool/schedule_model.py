import time
from multiprocessing import Process
from proxy_pool import web_model
from proxy_pool import get_model
from proxy_pool import check_model

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True


class Schedule(object):
    def schedule_tester(self):
        tester = check_model.Tester()
        while True:
            print("测试器开始运行")
            tester.run()
            time.sleep(TESTER_CYCLE)

    def schedule_getter(self):
        getter = get_model.Getter()
        while True:
            print("开始抓取代理")
            getter.run()
            time.sleep(GETTER_CYCLE)

    def schedule_web(self):
        web_model.app.run()

    def run(self):
        print("代理池开始运行")
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            web_process = Process(target=self.schedule_web)
            web_process.start()


if __name__ == "__main__":
    schedule = Schedule()
    schedule.run()
