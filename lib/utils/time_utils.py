#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/15 0015 上午 9:55
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import datetime

import pytz


class Timer():

    @staticmethod
    def now_time():
        return datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H-%M-%S")

    @staticmethod
    def is_in_yesterday(time):
        now = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
        oneday = datetime.timedelta(days=1)
        yesterday = (now - oneday).strftime("%Y-%m-%d")
        if time[:10] == yesterday[:10]:
            return True
        else:
            return False

