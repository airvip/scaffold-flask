#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件 :compute.py
@说明 :
@时间 :2021/01/14 16:43:09
@作者 :airvip
'''
import datetime

from sqlalchemy import (create_engine, func)


def fix_compute_follows():
    """
    计算修正关注人数
    """

    now_date_time = (datetime.datetime.now() + datetime.timedelta(hours=0)).strftime( '%Y-%m-%d %H:%M:%S' )
    engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3307/jdbc1?charset=utf8mb4")
    cur = engine.execute("SELECT COUNT(id) FROM base_user")
    ret = cur.fetchone()[0]
    # print(ret)
    print("截止 %s 总共有 %d 个用户" %(now_date_time, ret))


def get_schedule():
    # url = "http://diff.wang/pushvuid?num="+ str(10)
    # buff = BytesIO()
    # c = pycurl.Curl() # 实例化
    # c.setopt(c.URL, url) # 设置请求地址
    # c.setopt(c.WRITEDATA, buff) # 写入请求的数据
    # c.perform() # 执行操作
    # c.close() # 关闭实例
    # ret = json.loads(buff.getvalue().decode())
    # ret = buff.getvalue().decode()
    # print(ret)
    pass

    
    

def get_schedule_day():
    pass

   