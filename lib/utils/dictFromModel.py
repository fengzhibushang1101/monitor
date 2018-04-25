#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:25
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""


def dict_from_model(model):
    setting = {}
    for key in dir(model):
        if key.isupper():
            setting[key.lower()] = getattr(model, key)
    return setting