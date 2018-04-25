#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:15
 @Author  : yitian
 @Software: PyCharm
 @Description:
"""


import logging

import logging.handlers

import json
import logging
import logging.handlers

from config import settings

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        level_name = record.levelname
        if self.use_color and level_name in COLORS:
            level_name_color = COLOR_SEQ % (30 + COLORS[level_name]) + level_name + RESET_SEQ
            record.level_name = level_name_color
        return logging.Formatter.format(self, record)


class Logging(object):

    @staticmethod
    def get_logger(name=__name__, log_level="debug", log_file=None):
        log_level = Logging.get_log_level(log_level)
        logger_obj = logging.getLogger(name)

        if len(logger_obj.handlers) <= 0:
            if log_file is not None:
                handler = logging.FileHandler(log_file)
            else:
                handler = logging.StreamHandler()

            formatter = ColoredFormatter(
                "%(asctime)s\t%(process)d|%(threadName)s\t%(thread)d\t%(levelname)s\t%(module)s\t%(funcName)s:%(lineno)d\t%(message)s"
            )
            handler.setFormatter(formatter)

            logger_obj.addHandler(handler)
            logger_obj.setLevel(log_level)

        return logger_obj

    @staticmethod
    def get_log_level(log_level):
        log_level = getattr(logging, log_level.upper(), None)
        if log_level is None:
            raise Exception("No such log level.")
        return log_level


logger = Logging.get_logger('myweb', log_file=settings.log_file)
