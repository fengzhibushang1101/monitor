#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 下午 12:18
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""

import contextlib
from sqlalchemy.orm import sessionmaker
from lib.sql.base import db


session_maker = sessionmaker(bind=db)


def get_session():
    """
    链接到数据库的SESSION
    """
    return session_maker()


@contextlib.contextmanager
def sessionCM():
    session = get_session()
    try:
        yield session
    except Exception, e:
        raise
    finally:
        session.close()