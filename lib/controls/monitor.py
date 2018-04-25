#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/25 10:57
 @Author  : jyq
 @Software: PyCharm
 @Description: 
"""
import socket
import traceback

import paramiko

from lib.sql.monitor import Monitor
from lib.utils.error_utils import StdError
from lib.utils.logger_utils import logger


class MonitorControl(object):
    def __init__(self, public_ip, session):
        self.public_ip = public_ip
        self.session = session

    def is_in_record(self):
        return Monitor.find_by_public_ip(self.session, self.public_ip)

    def add_to_record(self, user_name, password, name, area, tags, service, description="", ssh_client=None):
        if not ssh_client:
            ssh_client = paramiko.SSHClient()
            # 设置为接受不在known_hosts 列表的主机可以进行ssh连接
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(hostname=self.public_ip, port=22, username=user_name, password=password)
            memory_capacity = self.exec_command(ssh_client, "free -m | grep Mem | awk '{print $2}'")
            disk_capacity = self.exec_command(ssh_client, "df -m | awk '{print $2}'| head -n 2 | tail -n 1")
            core_count = self.exec_command(ssh_client, "cat /proc/cpuinfo | grep 'cpu cores' | wc -l")
            cpu_count = self.exec_command(ssh_client, "cat /proc/cpuinfo | grep 'physical id' | wc -l")
            inner_ip = self.exec_command(ssh_client,
                                         "/sbin/ifconfig -a | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}' | head -n 1")
            Monitor.create(self.session, **{
                "name": name,
                "inner_ip": inner_ip,
                "public_ip": self.public_ip,
                "cpu_count": cpu_count,
                "core_count": core_count,
                "disk_capacity": disk_capacity,
                "memory_capacity": memory_capacity,
                "user_name": user_name,
                "pwd": password,
                "area": area,
                "description": description,
                "tags": tags,
                "service": service
            })
        except socket.error, e:
            logger.error("添加机器失败:%s" % e.message)
            logger.error(traceback.format_exc(e))
        except paramiko.ssh_exception.AuthenticationException, e:
            logger.error("添加机器失败:%s" % e.message)
            logger.error(traceback.format_exc(e))
        except StdError, e:
            logger.error("添加机器失败:%s" % e.message)
            logger.error(traceback.format_exc(e))
        finally:
            ssh_client.close()

    def get_usage(self):
        pass

    def add_usage_to_record(self):
        pass

    def exec_command(self, ssh, commannd):
        stdin, stdout, stderr = ssh.exec_command(commannd)
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        if str_err != "":
            raise StdError(str_err)
        return str_out.strip()
