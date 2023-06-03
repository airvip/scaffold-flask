#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_caching import Cache

from flask_jwt_extended import JWTManager

import redis
import logging
from logging.handlers import RotatingFileHandler

from app.config import config_map
from app.util.coverter import ReCoverter


# 创建数据库对象
db = SQLAlchemy()

# 创建 redis 连接对象
redis_obj = None

# 创建 cache 对象
cache = Cache()

# 创建 jwt 对象
jwt = JWTManager()


# 设置日志的记录级别
logging.basicConfig(level=logging.DEBUG) # 调试级别 debug
## 创建日志记录器，指明日志保存路径、每个日志文件的最大大小 100Kb、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
## 创建日志记录格式  日志等级 输入日志信息的文件名 行数  日志错误
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
## 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
## 为全局的日志工具对象 (flask app使用) 添加日志记录器
logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    """
    @description  :
    ---------
    @param  config_name: String 配置模式的名字 ("dev" ,"develop", "product")
    -------
    @Returns  :
    -------
    """
    app = Flask(__name__)

    # 设置 flask 的配置信息
    config_class = config_map[config_name]
    app.config.from_object(config_class)
    # print(app.config['SQLALCHEMY_DATABASE_URI'])

    # 使用 app 初始化 db
    db.init_app(app)
    

    # 初始化 redis 工具
    global redis_obj
    redis_obj = redis.StrictRedis(host = config_class.REDIS_HOST, port = config_class.REDIS_PORT)


    # 使用 app 初始化 cache
    cache.init_app(app)

    # 使用 app 初始化 jwt
    jwt.init_app(app)

    # 利用 flask-session, 将 session 数据保存到 redis 中
    Session(app)

    # 为 flask 补充 csrf 防护
    # 如果开启 csrf 就需要在请求的 header 头 或者 form 表单中添加 X-CSRFToken 字段
    # 值可以直接取 cookies 中的 csrf_token 值
    # js 取 document.cookie.match("\\bcsrf_token=([^;]*)\\b")[1]
    # csrf.init_app(app)

    # 为 flask 添加自定义的转换器
    app.url_map.converters["re"] = ReCoverter

    # 注册蓝图
    from app import api
    app.register_blueprint(api.bp, url_prefix='/api')

    from app import admin
    app.register_blueprint(admin.bp, url_prefix="/admin")

    # 注册提供静态文件的蓝图
    from app import html
    app.register_blueprint(html.html)

    return app

    