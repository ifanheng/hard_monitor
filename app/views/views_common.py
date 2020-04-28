#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/4/26 19:15
# 什么程序创建：PyCharm
# 作用：

import tornado.web
from app.tools.monitor import Monitor

from tornado.escape import utf8, _unicode
from tornado.util import unicode_type
from typing import Any
from concurrent.futures import ThreadPoolExecutor  # 线程池


class CommonHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(1000)  # 定义线程池

    def progress_status(self, val):
        """
        进度条按照使用率的大小来给定颜色
        """
        data = ""
        if 0 <= val < 25:
            data = " bg-success"  # 绿色
        if 25 <= val <= 50:
            dat = ""  # 默认是蓝色
        if 50 <= val < 75:
            data = " bg-warning"  # 橙色
        if 75 <= val <= 100:
            data = " bg-danger"  # 红色
        return data

    # 最近开始时间
    @property
    def started(self):
        m = Monitor()
        return m.lastest_start_time()

    # 最近登录用户
    @property
    def users(self):
        m = Monitor()
        return m.logined_users()

    # 默认render方法是不支持线程的，这里把它重载了，让其支持线程。这里重新起了个名字叫html
    def html(self, template_name: str, **kwargs: Any) -> "Future[None]":
        if self._finished:
            raise RuntimeError("Cannot render() after finish()")
        html = self.render_string(template_name, **kwargs)

        # Insert the additional JS and CSS added by the modules on the page
        js_embed = []
        js_files = []
        css_embed = []
        css_files = []
        html_heads = []
        html_bodies = []
        for module in getattr(self, "_active_modules", {}).values():
            embed_part = module.embedded_javascript()
            if embed_part:
                js_embed.append(utf8(embed_part))
            file_part = module.javascript_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    js_files.append(_unicode(file_part))
                else:
                    js_files.extend(file_part)
            embed_part = module.embedded_css()
            if embed_part:
                css_embed.append(utf8(embed_part))
            file_part = module.css_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    css_files.append(_unicode(file_part))
                else:
                    css_files.extend(file_part)
            head_part = module.html_head()
            if head_part:
                html_heads.append(utf8(head_part))
            body_part = module.html_body()
            if body_part:
                html_bodies.append(utf8(body_part))

        if js_files:
            # Maintain order of JavaScript files given by modules
            js = self.render_linked_js(js_files)
            sloc = html.rindex(b"</body>")
            html = html[:sloc] + utf8(js) + b"\n" + html[sloc:]
        if js_embed:
            js_bytes = self.render_embed_js(js_embed)
            sloc = html.rindex(b"</body>")
            html = html[:sloc] + js_bytes + b"\n" + html[sloc:]
        if css_files:
            css = self.render_linked_css(css_files)
            hloc = html.index(b"</head>")
            html = html[:hloc] + utf8(css) + b"\n" + html[hloc:]
        if css_embed:
            css_bytes = self.render_embed_css(css_embed)
            hloc = html.index(b"</head>")
            html = html[:hloc] + css_bytes + b"\n" + html[hloc:]
        if html_heads:
            hloc = html.index(b"</head>")
            html = html[:hloc] + b"".join(html_heads) + b"\n" + html[hloc:]
        if html_bodies:
            hloc = html.index(b"</body>")
            html = html[:hloc] + b"".join(html_bodies) + b"\n" + html[hloc:]
        # 就只是这里把return self.finish(html)改成了return self.write(html)
        return self.write(html)
