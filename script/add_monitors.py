#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/25 16:10
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""

import yaml

from lib.controls.monitor import MonitorControl
from lib.sql.session import sessionCM

with open("../monitor_list.yaml") as f:
    monitor_list = yaml.load(f.read())

with sessionCM() as session:
    for public_ip, data in monitor_list.iteritems():
        mc = MonitorControl(public_ip, session)
        if not mc.get_record():
            mc.add_to_record(data["user_name"], data["password"], data["name"], data["area"], tags=data["group"],
                             service=data.get("service", ""), description=data.get("description", ""))
