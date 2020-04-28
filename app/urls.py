#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/4/25 22:01
# 什么程序创建：PyCharm
# 作用：

from sockjs.tornado import SockJSRouter  # 定义websocket的路由
from app.views.views_index import IndexHandler
from app.views.views_log import LogHandler  # 导入日志监控视图
from app.views.views_real_time import RealTimeHandler
from app.views.views_test import TestHandler

# 配置路由视图映射规则
urls = [
           (r"/", IndexHandler),
           (r"/log/", LogHandler),
           (r"/test", TestHandler),
       ] + SockJSRouter(RealTimeHandler, "/real/time").urls
