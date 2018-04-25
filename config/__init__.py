#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:17
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""
import os

from config import developement
from config import production
from lib.utils.dict2object import Dict2Obj
from lib.utils.dictFromModel import dict_from_model

default_env = "development"

execute_env = os.environ.get("PROCESS_ENV", default_env)

env = execute_env.lower()

if env in ["production"]:
    config = production
else:
    config = developement

settings = Dict2Obj(dict_from_model(config))