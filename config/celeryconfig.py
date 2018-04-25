#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/28 0028 下午 8:45
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from kombu import Queue, Exchange

CELERY_DEFAULT_QUEUE = "default_queue"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default.queue"
CELERY_IGNORE_RESULT = True
CELERY_ACKS_LATE = True
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_RESULT_BACKEND = "amqp"
CELERY_EVENT_QUEUE_TTL = 10
CELERY_EVENT_QUEUE_EXPIRES = 10
CELERY_SEND_EVENTS = False
CELERYD_PREFETCH_MULTIPLIER = 2
# CELERYD_TASK_TIME_LIMIT = 3 * 10 * 60
# BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3 * 6 * 10 * 60}
# CELERYD_MAX_TASK_PER_CHILD = 500  # 内存泄漏时开启




CELERY_QUEUES = (
    Queue('default_queue', Exchange('default_queue'), routing_key='default_queue'),
    Queue('send_mail', Exchange('mail'), routing_key='send.mail', exchange_type="direct"),
    Queue('get_usage', Exchange('monitor'), routing_key='monitor', exchange_type="direct"),

)

CELERY_ROUTES = (
    # 发送邮件的队列
    {"task.mail.send_mail": {"routing_key": "send.mail", "queue": "send_mail"}},
    # 监控机器队列
    {"task.get_usage.get_usage": {"routing_key": "monitor", "queue": "get_usage"}},

)
#
# CELERYBEAT_SCHEDULE = {
#
# }
#
CELERY_IMPORTS = (
    "task.mail",
    "task.get_usage"
)

CELERY_SEND_TASK_ERROR_EMAILS = False


BROKER_URL = 'amqp://myweb:w251192185@localhost:5672/myweb'
