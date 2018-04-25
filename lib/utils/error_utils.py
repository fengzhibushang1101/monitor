#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 下午 12:02
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""


class NullArgumentException(Exception):
    msg = "some arguments is null"


class MissArgumentError(Exception):
    msg = "some required arguments not supported"


class ErrorArgumentError(Exception):
    msg = "some arguments of supported is wrong"


class RedisError(Exception):
    msg = "there is something wrong about redis"


__all__ = [
    NullArgumentException, MissArgumentError, ErrorArgumentError, RedisError
]