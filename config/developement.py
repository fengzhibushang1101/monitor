#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:26
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""


import os
LOG_PATH = 'd://logs/'
LOG_FILE = os.path.sep.join([LOG_PATH, 'myweb.log'])



# mysql configure
ECHO_SQL = False

DB = {
    "user": "myweb",
    "password": "!w251192185",
    "host": "127.0.0.1",
    "db_name": "myweb",
}

# redis configure
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ""
REDIS_MAX_CONNECTIONS = 1024

# master's emails
MASTER_EMAIL = ["fengzhibushang@163.com"]