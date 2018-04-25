#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/25 10:36
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""
from lib.sql.base import Base
import sqlalchemy as SA

STATUS = dict(
    ACTIVE=1,
    CONNECT_ERROR=2,
    AUTH_ERROR=3,
    OTHER_ERROR=4,
    STOPPED=5
)

LINE = dict(
    mongo=300,
    mysql=500
)


class UsageRecord(Base):
    __tablename__ = "usage_record"

    __table_args__ = (
        SA.Index("create_date_index", 'create_date'),
    )

    id = SA.Column(SA.BIGINT(), primary_key=True, autoincrement=True)
    online = SA.Column(SA.Boolean(), default=False)
    status = SA.Column(SA.Boolean(), default=False)
    cpu_usage = SA.Column(SA.String(32))
    memory_usage = SA.Column(SA.String(32))
    disk_usage = SA.Column(SA.String(32))
    mysql_cpu = SA.Column(SA.FLOAT)
    mongo_cpu = SA.Column(SA.FLOAT)
    other_service_status = SA.Column(SA.String(128))
    service = SA.Column(SA.Text())
    robot_id = SA.Column(SA.INTEGER, nullable=False)
    error_times = SA.Column



