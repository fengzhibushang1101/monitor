#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/25 10:28
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


class Monitor(Base):
    __tablename__ = "monitor"

    __table_args__ = (
        SA.UniqueConstraint('public_ip', name="unique_public_ip"),
    )

    id = SA.Column(SA.INTEGER, autoincrement=True, primary_key=True)
    name = SA.Column(SA.String(32))  # 名称
    status = SA.Column(SA.INTEGER, default=STATUS["ACTIVE"])
    inner_ip = SA.Column(SA.String(32))  # 内网IP
    public_ip = SA.Column(SA.String(32), nullable=False)  # 外网IP
    cpu_count = SA.Column(SA.INTEGER, nullable=False)  # cpu 数量
    core_count = SA.Column(SA.INTEGER, nullable=False)  # cpu 核数
    disk_capacity = SA.Column(SA.INTEGER, nullable=False)  # 硬盘大小
    memory_capacity = SA.Column(SA.INTEGER, nullable=False)  # 内存大小
    user_name = SA.Column(SA.String(32), nullable=False)
    pwd = SA.Column(SA.String(128))
    area = SA.Column(SA.String(32))  # 地区
    description = SA.Column(SA.String(128))
    tags = SA.Column(SA.String(128))
    service = SA.Column(SA.String(1024))  # 此主机运行服务，可考虑添加新表
    error_times = SA.Column(SA.INTEGER, default=0)

    @classmethod
    def find_by_public_ip(cls, session, public_ip):
        return session.query(cls).filter(cls.public_ip == public_ip).first()

    @classmethod
    def get_all_using_robot(cls, session):
        return session.query(cls).filter(cls.status != STATUS["STOPPED"]).all()
