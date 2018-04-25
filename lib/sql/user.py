#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/25 0025 上午 9:27
 @Author  : Administrator
 @Software: PyCharm
 @Description: 
"""
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash, check_password_hash
from lib.sql.base import Base
import sqlalchemy as SA

from lib.utils.logger_utils import logger


class User(Base):

    __tablename__ = "user"

    id = SA.Column(SA.INTEGER, autoincrement=True, primary_key=True)
    mobile = SA.Column(SA.String(64), nullable=False, unique=True, index=True)
    email = SA.Column(SA.String(64), nullable=False, index=True)
    password = SA.Column(SA.String(128), nullable=False)
    name = SA.Column(SA.String(64), nullable=True)

    def set_password(self, pw):
        self.password = generate_password_hash(pw, salt_length=16)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)

    @classmethod
    def create(cls, session, mobile, password, email=""):
        try:
            session.query(cls).filter(cls.mobile == mobile).one()
        except NoResultFound:
            user = User()
            user.mobile = mobile
            user.email = email
            user.set_password(password)
            session.add(user)
            session.commit()
            return user
        except MultipleResultsFound:
            logger.error("create user error with the multiple user founded in the user table.")
        else:
            return True

    @classmethod
    def find_by_id(cls, session, user_id):
        user = session.query(cls).filter(cls.id == user_id).first()
        return user

    @classmethod
    def find_by_mobile(cls, session, mobile):
        user = session.query(cls).filter(cls.mobile == mobile).first()
        return user