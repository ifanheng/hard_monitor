#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/4/26 14:04
# 什么程序创建：PyCharm
# 作用：

import json

from sockjs.tornado import SockJSConnection
from app.tools.monitor import Monitor


# 实时监控类
class RealTimeHandler(SockJSConnection):
    # 定义一个连接池，所有客户端的一个集合
    waiters = set()  # 集合，一个元素不重复的对象

    # 1、建立连接
    def on_open(self, request):
        try:
            # 建立连接是，把当前实例本身添加到waiters集合
            self.waiters.add(self)
        except Exception as e:
            print(e)

    # 2、发送消息
    def on_message(self, message):
        try:
            # 封装监控信息
            m = Monitor()
            data = dict()
            if message == "system":
                data = dict(
                    mem=m.mem(),
                    swap=m.swap(),
                    cpu=m.cpu(),
                    disk=m.disk(),
                    net=m.net(),
                    dt=m.dt()  # 信息获取的datetime
                )

            # 对消息进行处理，把新的消息推送到所有连接的客户端
            self.broadcast(self.waiters, json.dumps(data))  # 广播
        except Exception as e:
            print(e)

    # 3、关闭连接
    def on_close(self):
        try:
            # 移除当前实例
            self.waiters.remove(self)
        except Exception as e:
            print(e)
