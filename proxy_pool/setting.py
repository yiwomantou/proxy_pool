import logging
from logging import handlers
import datetime

REDIS_HOST = '120.78.212.251'
REDIS_PORT = 6379

# 日志的配置
logger = logging.getLogger()

# 日志的输出等级
logger.setLevel(logging.INFO)

# 日志的切割
rf_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7,
                                                       atTime=datetime.time(0, 0, 0, 0), encoding='utf-8')
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

f_handler = logging.FileHandler('error.log', encoding='utf-8')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)
