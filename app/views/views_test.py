#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/4/28 3:46
# 什么程序创建：PyCharm
# 作用：

import time

import tornado.gen  # tornado协程
import tornado.concurrent  # tornado并发处理

from app.views.views_common import CommonHandler


class TestHandler(CommonHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        time.sleep(5)
        self.write("<h1>测试页</h1>")
