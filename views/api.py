#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/14 0014 上午 10:03
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import traceback
import ujson as json

from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.concurrent import run_on_executor
from tornado.web import HTTPError

from lib.sql.monitor import Monitor
from lib.sql.session import sessionCM
from lib.utils.logger_utils import logger
from task.get_usage import get_usage
from task.mail import send_to_master
from views.base import BaseHandler


class ApiHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)

    @gen.coroutine
    def get(self, *args, **kwargs):
        logger_dict = {"args": args, "kwargs": kwargs, "params": self.params, "method": "POST"}
        interface = args[0]
        method_settings = {
        }
        if interface not in method_settings:
            raise HTTPError(404)
        try:
            response = yield method_settings[interface]()
            self.write(response)
        except Exception, e:
            logger_dict["traceback"] = traceback.format_exc(e)
            logger.error(logger_dict)
            send_to_master("API出错", json.dumps(logger_dict))
            self.write({"status": 0, "message": "获取失败"})
        finally:
            self.finish()

    @gen.coroutine
    def post(self, *args, **kwargs):
        logger_dict = {"args": args, "kwargs": kwargs, "params": self.params, "method": "POST"}
        try:
            interface = args[0]
            method_settings = {
                "all_monitor": self.get_all_current_monitor
            }
            response = yield method_settings[interface]()
            self.write(response)
            self.finish()
        except Exception, e:
            logger_dict["traceback"] = traceback.format_exc(e)
            logger.error(logger_dict)
            send_to_master("API出错", json.dumps(logger_dict))
            self.write({"status": 0, "message": "获取失败"})

    @run_on_executor
    def get_all_current_monitor(self):
        with sessionCM() as session:
            robots = Monitor.get_all_using_robot(session)
            for robot in robots:
                get_usage.delay(robot.public_ip)
        return {"status": 1, "message": "已经加入任务队列" }


if __name__ == "__main__":
    def get_all_current_monitor():
        with sessionCM() as session:
            robots = Monitor.get_all_using_robot(session)
            for robot in robots:
                get_usage.delay(robot.public_ip)
    #
    #
    # get_all_current_monitor()
    # import requests
    # requests.post("http://monitor.kisu.top/api/all_monitor")