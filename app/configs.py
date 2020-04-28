#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/4/25 22:01
# 什么程序创建：PyCharm
# 作用：

import os

# 获取当前文件所在的目录
root_path = os.path.dirname(__file__)

# 配置文件
configs = dict(
    debug=True,  # 指定调试（开发者）模式
    template_path=os.path.join(root_path, "templates"),  # 模板文件存放路径
    static_path=os.path.join(root_path, "static")  # 静态文件存放路径
)
