#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/15 0015 上午 9:20
 @Author  : Administrator
 @Software: PyCharm
 @Description:
"""
from lib.sql.base import Base
import sqlalchemy as SA


class Jx3DailyRecord(Base):

    __tablename__ = "jx3_daily_record"

    id = SA.Column(SA.INTEGER, autoincrement=True, primary_key=True)
    update_time = SA.Column(SA.DateTime, nullable=False)
    info = SA.Column(SA.String(1024), nullable=False, default="")


