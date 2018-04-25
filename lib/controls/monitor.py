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

from lib.sql.monitor import Monitor, STATUS
from lib.sql.usage_record import LINE, UsageRecord
from lib.utils.error_utils import StdError, OverloadError
from lib.utils.logger_utils import logger
from task.mail import send_to_master


class MonitorControl(object):
    def __init__(self, public_ip, session):
        self.public_ip = public_ip
        self.session = session

    def get_record(self):
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
        with paramiko.SSHClient() as ssh:
            record = self.get_record()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(hostname=self.public_ip, port=22, username=record.user_name, password=record.pwd)
                cpu_reset = self.exec_command(ssh, "top -bn 1 -i -c|grep Cpu|awk -F, '{print $4}'| awk -Fi '{print $1}'")
                server_load = self.exec_command(ssh,
                                                "uptime | sed 's/.*average://g' | sed 's/\s*//g'| awk -F, '{print $1}'")
                memory_rest = self.exec_command(ssh, "free -m | grep Mem | awk '{print $7}'")
                disk_usage = self.exec_command(ssh, "df -m | awk '{print $3}'| head -n 2 | tail -n 1")
                mysql_cpu = self.exec_command(ssh, "top -b -n 1 | grep mysqld | awk '{b+=$9}END{print b}'")
                mongo_cpu = self.exec_command(ssh, "top -b -n 1 | grep mongod | awk '{b+=$9}END{print b}'")
                UsageRecord.create(self.session, **{
                    "cpu_usage": 1 - float(cpu_reset.strip().strip("%")) / 100,
                    "server_load": server_load,
                    "memory_usage": 1 - float(float(memory_rest) / record.memory_capacity),
                    "disk_usage": float(float(disk_usage) / record.disk_capacity),
                    "mysql_cpu": float(mysql_cpu or 0),
                    "mongo_cpu": float(mongo_cpu or 0),
                    "robot_id": record.id
                })
                record.error_times = 0
                record.status = STATUS["ACTIVE"]
                if mysql_cpu and float(mysql_cpu) > LINE["mysql"]:
                    raise OverloadError
                if mongo_cpu and float(mongo_cpu) > LINE["mysql"]:
                    raise OverloadError
            except OverloadError, e:
                send_to_master("服务器%s负载过高" % record.name,
               "%s机器数据库负载过高当前机器状态为\n系统负载:%f\nCPU使用率:%f\n内存使用率:%f\n硬盘使用率:%f\nmysql CPU占用:%f\nmongo CPU占用:%f" % (
                               record.name, record.server_load, record.cpu_usage, record.memory_usage,
                               record.disk_usage, record.mysql_cpu, record.mongo_cpu))
            except socket.error, e:
                record.error_times += 1
                record.status = STATUS["CONNECT_ERROR"]
                logger.error("获取状态信息失败:%s" % e.message)
                logger.error(traceback.format_exc(e))
            except paramiko.ssh_exception.AuthenticationException, e:
                record.error_times += 1
                record.status = STATUS["AUTH_ERROR"]
                logger.error("获取状态信息失败:%s" % e.message)
                logger.error(traceback.format_exc(e))
            except StdError, e:
                record.error_times += 1
                record.status = STATUS["OTHER_ERROR"]
                logger.error("获取状态信息失败:%s" % e.message)
                logger.error(traceback.format_exc(e))
            except Exception, e:
                self.session.rollback()
                record.error_times += 1
                record.status = STATUS["OTHER_ERROR"]
                print traceback.format_exc(e)
                logger.error("获取状态信息失败:%s" % e.message)
                logger.error(traceback.format_exc(e))
            finally:
                if record.error_times > 5:
                    record.status = STATUS["STOPPED"]
                    send_to_master("API出错", "%s机器连续五分钟获取不到信息, 设置状态为stop!" % record.name)
                self.session.add(record)
                self.session.commit()

    def add_usage_to_record(self):
        pass

    def exec_command(self, ssh, commannd):
        stdin, stdout, stderr = ssh.exec_command(commannd)
        str_out = stdout.read().decode()
        str_err = stderr.read().decode()
        if str_err != "":
            raise StdError(str_err)
        return str_out.strip()


if __name__ == "__main__":
    from lib.sql.session import sessionCM
    with sessionCM() as session:
        MonitorControl("180.76.98.136", session).get_usage()