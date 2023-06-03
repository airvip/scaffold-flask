#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import session, jsonify, g
from app.util.response_code import RET
# python 提供的标准模块
import functools

# 定义的验证登录状态的装饰器
def login_required(view_func):
    
    # 加上之后就不会改变被装饰的函数的相关属性
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户的登录状态
        user_id = session.get("user_id")
        # 如果用户是登录的，执行视图函数
        if user_id is not None:
            # 将 user_id 保存到 g 对象中，在视图函数中可以通过 g 对象获取保存数据
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            # 如果未登录，返回未登录的信息
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    return wrapper