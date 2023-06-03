#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from celery import Celery
from . import config

# 定义 celery 对象
celery_app = Celery("app")

# 引入配置信息
celery_app.config_from_object(config)
# 不导入 config, 可以使用下面这句话代替
# celery_app.config_from_object('app.tasks.config')

# 自动搜寻异步任务
celery_app.autodiscover_tasks(["app.tasks.sms"])