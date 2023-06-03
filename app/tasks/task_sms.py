#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from celery import Celery
from app.util.netease_sms_sdk import NeteaseSmsApi as sms
from flask import current_app

celery_app = Celery("app", broker="redis://127.0.0.1:6379/1")

@celery_app.task
def send_code(mobile):
    """
    @description : 异步发送短信任务
    """
    try:
        api = sms()
        ret = api.send_code(mobile)
    except Exception as e:
        current_app.logger.error(e)


@celery_app.task
def send_temp(template_id, mobiles, data):
    """
    @description : 异步发送短信任务
    ---------
    @param template_id: 模板id
    @param mobiles: 手机号 "13108765051" 或者 ['13108765051', '13208765051']
    @param data: 模板变量替换值 ['airvip', 'hello']
    -------
    """
    try:
        api = sms()
        api.send_template(template_id, mobiles, data)
    except Exception as e:
        current_app.logger.error(e)