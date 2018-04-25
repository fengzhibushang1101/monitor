#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/12 0012 下午 9:12
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""

import sqlalchemy as SA

from lib.sql.base import Base


class GifList(Base):
    __tablename__ = "gif_list"

    id = SA.Column(SA.INTEGER, autoincrement=True, primary_key=True)
    name = SA.Column(SA.String(64), nullable=False, unique=True, index=True)
    path = SA.Column(SA.String(64), nullable=False, default="")
    length = SA.Column(SA.INTEGER, nullable=False)
    extra = SA.Column(SA.String(64), default="")

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter(cls.name == name).first()

    @classmethod
    def get_names(cls, session):
        return [info.name for info in session.query(cls.name).all()]


if __name__ == "__main__":
    gif_list = [["wangjingze", 4], ["sorry", 9]]
    from lib.sql.session import sessionCM

    with sessionCM() as session:
        for gif_info in gif_list:
            GifList.create(session, **{"name": gif_info[0], "length": gif_info[1]})
