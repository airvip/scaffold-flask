#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件 :__init__.py
@说明 :
@时间 :2020/12/25 18:07:33
@作者 :airvip
'''

from app import db
import datetime,time

class BaseModel(object):
    """
    @description  : 模型基类，为每个模型补充创建时间与更新时间
    ---------
    """
    now_date_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    # datetime.datetime.now() 默认的是 UTC 时间，后面转换要 +8 小时到北京时间,为了方便我们直接在插入的时候 +8 小时
    # create_time = db.Column(db.DateTime, default=datetime.datetime.now) # 记录创建时间
    # update_time = Column(db.TIMESTAMP, nullable=False, comment='更新时间戳')
    create_time = db.Column(db.DateTime, nullable=False, default=now_date_time, comment='创建时间') 
    update_time = db.Column(db.DateTime, nullable=True,  onupdate=now_date_time, comment='更新时间') 

    







from app.model.user_role import user_role, RoleModel, UserModel