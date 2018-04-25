#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/25 10:57
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""
import socket

import paramiko

from lib.sql.monitor import Monitor
from lib.utils.error_utils import StdError


class MonitorControl(object):

    def __init__(self, public_ip, session):
        self.public_ip = public_ip
        self.session = session

    def is_in_record(self):
        return Monitor.find_by_public_ip(self.session, self.public_ip)

    def add_to_record(self, user_name, password, ssh_client=None):
        if not ssh_client:
            ssh_client = paramiko.SSHClient()
            # 设置为接受不在known_hosts 列表的主机可以进行ssh连接
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print self.public_ip
            print user_name
            print password
            ssh_client.connect(hostname=self.public_ip, port=22, username=user_name, password=password)
            memory_capacity = self.exec_command(ssh_client, "free -m | grep Mem | awk '{print $2}'")
            disk_capacity = ""
            core_count = ""
            cpu_count = ""
            inner_ip = ""
        except socket.error, e:
            print e.message
        except StdError, e:
            print e.message


    def exec_command(self, ssh, commannd):
        stdin, stdout, stderr = ssh.exec_command(commannd)
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        if str_err != "":
            raise StdError(str_err)
        return str_out


if __name__ == "__main__":
    from lib.sql.session import sessionCM

    with sessionCM() as session:
        mc = MonitorControl("47.254.16.204", session)
        print mc.add_to_record('odin', 'Ww#251192185')



