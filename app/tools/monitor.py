#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/4/25 23:31
# 什么程序创建：PyCharm
# 作用：

import psutil
import time
import datetime
import os
from pprint import pprint


# 定义一个专门用于获取系统信息的类
class Monitor(object):
    # 专门用于单位转化的方法
    def bytes_to_gb(self, data, key=""):
        """
        把字节转换成gb
        """
        if key == "percent":
            # 但是当传入key="percent"时，就直接返回原始数据
            return data
        else:
            # 默认这返回的是字节转GB的数据
            return round(data / (1024 * 1024 * 1024), 2)  # round保留两位小数点

    # 专门获取内存信息
    def mem(self):
        # 内存信息
        info = psutil.virtual_memory()
        data = dict(
            total=self.bytes_to_gb(info.total),
            used=self.bytes_to_gb(info.used),
            free=self.bytes_to_gb(info.free),
            percent=info.percent
        )
        return data

    # 专门获取交换分区/文件信息
    def swap(self):
        # 交换文件/分区信息
        info = psutil.swap_memory()
        data = dict(
            total=self.bytes_to_gb(info.total),
            free=self.bytes_to_gb(info.free),
            used=self.bytes_to_gb(info.used),
            percent=info.percent
        )
        return data

    # 专门获取CPU信息
    def cpu(self):
        # percpu：True获取每个CPU的使用率，False获取平均使用率
        # 1.平均、2.单独、3.物理CPU核心数、4.逻辑CPU核心数
        data = dict(
            percent_avg=psutil.cpu_percent(interval=0, percpu=False),
            percent_per=psutil.cpu_percent(interval=0, percpu=True),
            num_p=psutil.cpu_count(logical=False),
            num_l=psutil.cpu_count(logical=True)
        )
        return data

    # 专门获取磁盘信息
    def disk(self):
        # 专门获取磁盘分区信息
        info = psutil.disk_partitions()
        data = []
        for device in info:
            used_dict = {}
            if os.name == 'nt':
                if 'cdrom' in device.opts or device.fstype == '':
                    # 跳过windows机器上的cd-rom驱动器(将抛出错误)
                    continue
                # 把这种sdiskusage(total=564835381248, used=487340969984, free=77494411264, percent=86.3)转换成
                # 字典{'free': 72.17, 'percent': 86.3, 'total': 526.04, 'used': 453.87}
                for k, v in psutil.disk_usage(device.mountpoint)._asdict().items():
                    used_dict[k] = self.bytes_to_gb(v, k)

            data.append(
                {
                    "device": device.device,
                    "mountpoint": device.mountpoint,
                    "fstype": device.fstype,
                    "used": {**used_dict}
                }
            )
        return data

    # 专门获取网络信息
    def net(self):
        # 获取地址信息
        addrs = psutil.net_if_addrs()
        # val.family.name取出协议地址族名称，AF_INET
        addrs_info = {
            k: [
                dict(
                    family=val.family.name,
                    address=val.address,
                    netmask=val.netmask,
                    broadcast=val.broadcast
                )
                for val in v if val.family.name == "AF_INET"
            ][0]
            for k, v in addrs.items()
        }
        # 获取输入输出信息（收发包数，收发字节数）
        io = psutil.net_io_counters(pernic=True)
        data = [
            dict(
                name=k,
                bytes_sent=v.bytes_sent,
                bytes_recv=v.bytes_recv,
                packets_sent=v.packets_sent,
                packets_recv=v.packets_recv,
                **addrs_info[k]
            )
            for k, v in io.items()
        ]
        return data

    # 时间戳转化为时间字符方法
    def td(self, tm):
        dt = datetime.datetime.fromtimestamp(tm)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # 获取日期时间
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 获取日期时间
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 专门获取最近开机时间
    def lastest_start_time(self):
        # 时间戳
        return self.td(psutil.boot_time())

    # 专门获取系统登录用户
    def logined_users(self):
        users = psutil.users()
        data = [
            dict(
                name=v.name,
                terminal=v.terminal,
                host=v.host,
                started=self.td(v.started),
                pid=v.pid
            )
            for v in users
        ]
        return data


if __name__ == '__main__':
    m = Monitor()
    pprint(m.dt())
    pprint(m.lastest_start_time())
    pprint(m.logined_users())
