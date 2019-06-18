# coding:utf-8

import logging


class Logger(object):
    def __init__(self, file_name):
        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(logging.DEBUG)
        # 设置文件日志
        fh = logging.FileHandler('./log/report.log')
        fh.setFormatter(fmt)
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

    def exception(self, e):
        self.logger.exception(e)
