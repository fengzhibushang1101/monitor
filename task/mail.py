#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/28 0028 下午 8:55
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""

import traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from config import settings
from lib.utils.logger_utils import logger
from task import celery


@celery.task(ignore_result=True)
def send_mail(subject,
              text,
              to=list(),
              cc=list(),
              bcc=list(),
              name='smtp.qq.com',
              account='714285795@qq.com',
              password='qjfhafovyykpbbfg'
              ):
    """
    发关邮件的后台任务可以单独调用
    """
    assert type(to) == list
    assert type(cc) == list
    assert type(bcc) == list

    fro = "网站myweb<%s>" % account
    real_to = to
    msg = MIMEMultipart()
    msg["From"] = fro
    msg["Subject"] = subject
    msg["To"] = COMMASPACE.join(to)
    if cc:
        msg["Cc"] = COMMASPACE.join(cc)
        real_to += cc

    if bcc:
        msg["Bcc"] = COMMASPACE.join(bcc)
        real_to += bcc
    msg["Date"] = formatdate(localtime=True)

    if isinstance(text, dict):
        text_group = list()
        for k, v in text.iteritems():
            text_group.append("%s:%s" % (str(k), str(v)))
        text = ";".join(text_group)

    msg.attach(MIMEText(text, "html", _charset="UTF8"))

    try:
        auth_info = {"name": name, "user": account, "passwd": password}
        smtp = smtplib.SMTP_SSL(auth_info["name"], 465, timeout=20)
        smtp.login(auth_info["user"], auth_info["passwd"])
        smtp.sendmail(fro, real_to, msg.as_string())
        smtp.quit()

    except Exception, e:
        logger.info("this time is to send content: %s" % text)
        logger.info(traceback.format_exc(e))


def send_to_master(title, content):
    send_mail.delay(title, content, to=settings.master_email)