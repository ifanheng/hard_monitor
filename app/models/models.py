#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/4/25 22:30
# 什么程序创建：PyCharm
# 作用：

"""
1、导入模型继承父类
2、导入数据类型
3、导入创建字段类
4、定义模型
"""

from sqlalchemy.ext.declarative import declarative_base  # 模型继承父类
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL, DATE, TIME, DATETIME  # 导入字段
from sqlalchemy import Column  # 导入创建字段的类

Base = declarative_base()  # 调用模型继承父类
metadata = Base.metadata  # 创建元类


# 定义模型
class Mem(Base):
    """
    内存统计模型
    分析字段：
    编号 id 大整型 主键
    使用率 percent 小数类型 允许为空
    总容量 total 小数类型 允许为空
    使用量 used 小数类型 允许为空
    剩余量 free 小数类型 允许为空
    创建日期 create_date 日期类型
    创建时间 create_time 时间类型
    创建日期时间 create_dt 日期时间类型
    """
    __tablename__ = "mem"  # 指定表名称
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    total = Column(DECIMAL(8, 2))
    used = Column(DECIMAL(8, 2))
    free = Column(DECIMAL(8, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


class Swap(Base):
    """
    交换分区
    分析字段：
    编号 id 大整型 主键
    使用率 percent 小数类型 允许为空
    总容量 total 小数类型 允许为空
    使用量 used 小数类型 允许为空
    剩余量 free 小数类型 允许为空
    创建日期 create_date 日期类型
    创建时间 create_time 时间类型
    创建日期时间 create_dt 日期时间类型
    """
    __tablename__ = "swap"  # 指定表名称
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    total = Column(DECIMAL(8, 2))
    used = Column(DECIMAL(8, 2))
    free = Column(DECIMAL(8, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


class Cpu(Base):
    """
    CPU统计
    分析字段：
    编号 id 大整型 主键
    使用率 percent 小数类型 允许为空
    创建日期 create_date 日期类型
    创建时间 create_time 时间类型
    创建日期时间 create_dt 日期时间类型
    """
    __tablename__ = "cpu"  # 指定表名称
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


if __name__ == '__main__':
    # 1、导入数据库连接驱动
    import mysql.connector
    # 2、导入创建引擎
    from sqlalchemy import create_engine

    # 配置一下连接信息
    mysql_configs = dict(
        db_host="localhost",
        db_name="hard_monitor",
        db_port=3306,
        db_user="root",
        db_pwd="abc,123"
    )
    """
    连接格式：mysql+驱动名称://用户:密码@主机:端口/数据库名称
    """
    link = "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}".format(
        **mysql_configs
    )

    # 创建连接引擎，encoding定义编码，echo是否输出日志
    engine = create_engine(link, encoding="utf-8", echo=True)

    # 映射
    metadata.create_all(engine)
