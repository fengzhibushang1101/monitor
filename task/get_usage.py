#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/25 0025 下午 9:40
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
import celery

from lib.controls.monitor import MonitorControl
from lib.sql.session import sessionCM


@celery.task(ignore_result=True)
def get_usage(public_ip):
    with sessionCM() as session:
        MonitorControl(public_ip, session).get_usage()

