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

from lib.controls.jx3info import Jx3Info
from lib.utils.logger_utils import logger
from task.mail import send_to_master
from views.base import BaseHandler


class ApiHandler(BaseHandler):
    executor = ThreadPoolExecutor(10)

    @gen.coroutine
    def get(self, *args, **kwargs):
        logger_dict = {"args": args, "kwargs": kwargs, "params": self.params, "method": "POST"}
        interface = args[0]
        method_settings = {
            "jx3/info": self.get_jx3info
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
                "jx3/info": self.update_jx3_info
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
    def get_jx3info(self):
        return {"status": 1, "info": Jx3Info.get_info()}

    @run_on_executor
    def update_jx3_info(self):
        res = Jx3Info.auto_add_one()
        if res:
            return {"status": 1, "message": "更新成功"}
