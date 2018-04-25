#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:20
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""


class Dict2Obj(object):

    def __init__(self, d):
        if isinstance(d, dict):
            for k, v in d.iteritems():
                self.__setattr__(k, v)

    def configure(self, k, v):
        self.__setattr__(k.lower(), v)