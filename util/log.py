# -*- coding: utf-8 -*-
import os
import logging.handlers

# log_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'logs'
log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)

# CONSTANT VARIABLES

MODULE_NAME = 'my_module'
LOG_LEVEL = 'INFO'


def get_logger(module_name=MODULE_NAME, log_level=LOG_LEVEL):

    logging.basicConfig()

    logger = logging.getLogger(module_name)

    logger.setLevel(log_level)

    # 按时间回滚 1天换1次, 保留180天
    time_file_handler = logging.handlers.TimedRotatingFileHandler(
        log_dir + os.sep + module_name + '_day.log',
        when='midnight',
        interval=1,
        backupCount=180
    )

    time_file_handler.suffix = '%Y-%m-%d.log'  # 按 天

    formatter = logging.Formatter(
        '[%(asctime)s]-[%(pathname)s]-[%(funcName)s]-[%(lineno)d] - [%(levelname)s]: %(message)s')
    time_file_handler.setFormatter(formatter)

    logger.addHandler(time_file_handler)

    sh = logging.StreamHandler()  # 往屏幕上输出
    sh.setFormatter(formatter)  # 设置屏幕上显示的格式
    logger.addHandler(sh)  # 把对象加到logger里

    return logger

