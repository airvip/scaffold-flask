#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import redis

class Config(object):
    """配置信息"""
    SECRET_KEY = "AIRVip123456airvip"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/scaffold-flask"
    # 如果设置成 True (默认),Flask-SQLAlchemy 将会追踪对象的修改并且发送信号,需要额外的内存。
    # 如果不必要，可以禁用。
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 开发模式开启可以查看 sql 语句
    SQLALCHEMY_ECHO = True  



    # redis
    REDIS_HOST = "127.0.0.1" # home
    REDIS_PORT = 6379

    # cache
    CACHE_TYPE = "redis"
    CACHE_DEFAULT_TIMEOUT = 7200
    CACHE_KEY_PREFIX = 'fl_'
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 1

    # JWT
    # JWT_REFRESH_TOKEN_EXPIRES = 7200
    JWT_ACCESS_TOKEN_EXPIRES = 7200
    # SECRET_KEY = "HS256"

    # session
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT)
    SESSION_USE_SIGNER = True # 对 cookie 中的 session_id 进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 86400 # session 数据的有效期，单位 秒

class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境的配置信息"""
    pass

config_map = {
    "dev": DevelopmentConfig,
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}