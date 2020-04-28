#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/4/25 22:15
# 什么程序创建：PyCharm
# 作用：

import tornado.web
import tornado.gen  # tornado协程
import tornado.concurrent  # tornado并发处理

from app.tools.monitor import Monitor
from app.tools.chart import Chart

from app.views.views_common import CommonHandler


class IndexHandler(CommonHandler):
    """
    首页视图
    """

    # 以装饰器的方式使用协程
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()

    # 把阻塞的代码，写进线程里面
    @tornado.concurrent.run_on_executor
    def get_response(self):
        # self.write("<h1>我们要开发一个硬件实时监控系统</h1>")
        m = Monitor()
        c = Chart()
        cpu_info = m.cpu()
        mem_info = m.mem()
        swap_info = m.swap()
        net_info = m.net()
        disk_info = m.disk()
        # print(cpu_info)
        net_pie = [
            c.pie_two_html(
                "net{}".format(k + 1),
                "{}网卡信息".format(v["name"]),
                "收发包数统计",
                "收发字节统计",
                ["收包数", "发包数"],
                ["收字节", "发字节"],
                [v["packets_recv"], v["packets_sent"]],
                [v["bytes_recv"], v["bytes_sent"]],
            )
            for k, v in enumerate(net_info) if v["packets_recv"] and v["packets_sent"]  # 只接收有收包数和发包数的网卡信息
        ]
        # 这里我们在views_common.py的CommonHandler里面重载的render方法：html
        self.html("index.html",
                    data=dict(
                        title="系统监控",
                        cpu_info=cpu_info,
                        mem_info=mem_info,
                        swap_info=swap_info,
                        net_info=net_info,
                        disk_info=disk_info,
                        cpu_liquid=c.liquid_html("cpu_avg", "CPU平均使用率", cpu_info["percent_avg"]),
                        mem_gauge=c.gauge_html("mem", "内存使用率", mem_info["percent"]),
                        swap_gauge=c.gauge_html("swap", "交换分区使用率", swap_info["percent"]),
                        net_pie=net_pie,
                    )
                    )
