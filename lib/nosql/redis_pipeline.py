#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/15 0015 上午 9:24
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from redis import WatchError

from lib.nosql.redis_util import conn


class PipeLineCommand(object):

    def __init__(self, t, key, v=None):
        self.type = t
        self.key = key
        self.value = v


class RedisPipeline(object):

    def __init__(self):
        self.conn = conn
        self.pipe = self.conn.pipeline()

    def set(self, key, value=None):
        return self.pipe.set(key, value)

    def get(self, key=None):
        return self.pipe.get(key)

    def watch(self, key):
        return self.pipe.watch(key)

    def execute(self):
        return self.pipe.excute()

    def reset(self):
        return self.pipe.reset()

    def multi_set(self, commands):
        watch_keys = set([command.key for command in commands])
        try:
            self.pipe.watch(*watch_keys)
            for command in commands:
                pass
        except WatchError:
            pass
        finally:
            self.pipe.reset()





