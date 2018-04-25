#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/24 0024 下午 12:47
 @Author  : yitian
 @Software: PyCharm
 @Description: 
"""
import functools
import urlparse
from urllib import urlencode

from tornado.web import HTTPError
from torndsession.sessionhandler import SessionBaseHandler
from tornado.escape import to_unicode

from lib.sql.session import sessionCM
from lib.sql.user import User
from lib.utils.logger_utils import logger


class BaseHandler(SessionBaseHandler):
    """Implements Google Accounts authentication methods."""

    def get(self, *args, **kwargs):
        self.on_request()

    def post(self, *args, **kwargs):
        self.on_request()

    @property
    def params(self):
        return self._argument()

    @property
    def cookies(self):
        return self._cookies()

    @property
    def headers(self):
        return self._headers

    def _argument(self):
        return self._flatten_arguments(self.request.arguments)

    def _flatten_arguments(self, args):
        """
        去除请求中单值参数的数组结构

        """
        flattened = {}
        for key in args:
            if len(args[key]) == 1:
                flattened[key] = self.str_to_unicode(args[key][0])
            else:
                flattened[key] = [self.str_to_unicode(arg) for arg in args[key]]

        return flattened

    def _cookies(self):
        cookies = dict()
        cookie_str = self.request.headers.get("Cookie")
        for cookie in cookie_str.split(";"):
            name, value = cookie.strip().split("=", 1)
            cookies[name] = value
        return cookies

    @staticmethod
    def str_to_unicode(word):
        try:
            return to_unicode(word)
        except Exception, e:
            logger.info(e.message)
            return word.decode("unicode-escape")

    def on_request(self):
        logger.info(self.request.arguments)
        logger.info(self.request.full_url())
        logger.info(self.request.headers["X-Real-IP"])
        logger.info(self.session.get("user_id"))
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        self.write(str(status_code))

    def get_current_user(self):
        try:
            user_id = self.session["user_id"]
            with sessionCM() as session:
                user = User.find_by_id(session, user_id)
                return user
        except Exception, e:
            logger.info(e.message)

    def gen_render_settings(self):
        user = self.current_user
        render_settings = dict()
        if not user:
            render_settings["name"] = ""
        else:
            render_settings["name"] = user.name if user.name else "游客:%s" % user.id
        return render_settings



def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.

    If you configure a login url with a query parameter, Tornado will
    assume you know what you're doing and use it as-is.  If not, it
    will add a `next` parameter so the login page knows where to send
    you once you're logged in.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper

