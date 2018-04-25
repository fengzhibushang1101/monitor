#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:25
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""



# log configure
import os

LOG_PATH = '/home/odin/log/myweb/'
LOG_FILE = os.path.sep.join([LOG_PATH, 'myweb.log'])
DEFAULT_LOG_SIZE = 1024*1024*50

# mysql configure
ECHO_SQL = False

DB = {
    "user": "myweb",
    "password": "MyNewPass4!",
    "host": "127.0.0.1",
    "db_name": "myweb",
}

# redis configure
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = "n1UUi4IKc1m2hV277eZtYW9T451p5lV3tSHAFJ647Xai83U44izwm2ciXDrxt05p"
REDIS_MAX_CONNECTIONS = 1024

# master's emails
MASTER_EMAIL = ["fengzhibushang@163.com"]
