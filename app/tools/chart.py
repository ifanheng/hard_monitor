#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/4/26 16:07
# 什么程序创建：PyCharm
# 作用：

import datetime
from pyecharts import options as opts
from pyecharts.charts import Liquid, Gauge, Pie, Line


class Chart(object):
    # 日期时间的方法
    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 水球图
    def liquid_html(self, chart_id, title, val):
        # 基本配置
        liquid = Liquid(init_opts=opts.InitOpts(width="100%", height="300px"))
        liquid.set_global_opts(
            title_opts=opts.TitleOpts(
                title="{}-{}".format(self.dt, title),
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(font_size=14, color="white")
            ),
        )
        # 绑定id
        liquid.chart_id = chart_id
        # 添加参数
        liquid.add("", [round(val / 100, 4)])
        return liquid.render_embed()  # 返回图表html代码

    # 仪表图
    def gauge_html(self, chart_id, title, val):
        gauge = Gauge(init_opts=opts.InitOpts(width="100%", height="300px"))
        gauge.set_global_opts(
            title_opts=opts.TitleOpts(
                title="{}-{}".format(self.dt, title),
                title_textstyle_opts=opts.TextStyleOpts(color="white", font_size=14),
                pos_left="center"
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        # 绑定id
        gauge.chart_id = chart_id
        gauge.add(
            series_name="",
            data_pair=[["", val]],
            title_label_opts=opts.LabelOpts(color="white"),
        )

        return gauge.render_embed()  # 返回图表html代码

    # 饼状图
    def pie_two_html(self, chart_id, title, sub_title1, sub_title2, key1, key2, val1, val2):
        # 实例化饼状图
        pie = Pie(init_opts=opts.InitOpts(width="100%", height="300px"))
        pie.set_global_opts(
            title_opts=opts.TitleOpts(
                title="{}-{}".format(self.dt, title),
                title_textstyle_opts=opts.TextStyleOpts(color="white", font_size=14),
                pos_left="center"
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        pie.chart_id = chart_id
        # print("key1: %s" % key1)
        # print("val1: %s" % val1)
        pie.add(
            sub_title1,
            [list(z1) for z1 in zip(key1, val1)],
            center=[300, 160],
            radius=[30, 75],
        )
        pie.add(
            sub_title2,
            [list(z2) for z2 in zip(key2, val2)],
            center=[1100, 160],
            radius=[30, 75],
        )

        return pie.render_embed()

    # 折线-面积图
    def line_html(self, title, key, val, color=None):
        line = Line(init_opts=opts.InitOpts(width="100%", height="300px"))
        line.set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                title_textstyle_opts=opts.TextStyleOpts(color="black", font_size=14),
                pos_left="center",
            ),
            # 增添x，y轴以及内部的缩放
            datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100)],
        )
        line.add_xaxis(key)
        line.add_yaxis(
            "",
            val,
            symbol=None,
            is_symbol_show=False,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color=color),
            linestyle_opts=opts.LineStyleOpts(opacity=0.2),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="average", name="平均值"),
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),

                    opts.MarkLineItem(type_="average", name="平均值"),
                    opts.MarkLineItem(type_="max", name="最大值"),
                    opts.MarkLineItem(type_="min", name="最小值"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="average", name="平均值"),
                    opts.MarkLineItem(type_="max", name="最大值"),
                    opts.MarkLineItem(type_="min", name="最小值")
                ]
            ),
            is_selected=True,
            is_smooth=True,
            is_hover_animation=True,
        )

        return line.render_embed()

    # 折线图(这里设计个三层折线图)
    def line_three_html(self, title, key, val_min, val_max, val_avg):
        line = Line(init_opts=opts.InitOpts(width="100%", height="300px"))
        line.set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                title_textstyle_opts=opts.TextStyleOpts(color="black", font_size=14),
                pos_left="left",
            ),
            # 增添x，y轴以及内部的缩放
            datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100)],
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True))
        )
        line.add_xaxis(key)
        line.add_yaxis(
            "最小值",
            val_min,
            is_smooth=True,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ),
        )
        line.add_yaxis(
            "最大值",
            val_max,
            is_smooth=True,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ),
        )
        line.add_yaxis(
            "平均值",
            val_avg,
            is_smooth=True,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ),
        )

        return line.render_embed()
