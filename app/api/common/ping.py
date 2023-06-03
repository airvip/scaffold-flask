#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from app.api import bp
from flask import g, current_app
from flasgger import swag_from

@bp.route('/ping/<string:name>', methods=['GET'])
@swag_from('/app/docs/api/common/ping.yml')
def ping(name):
    return "pong {}".format(name)


@bp.route('/mobile/<re(r"1[3-9]\d{9}"):mobile>')
@swag_from('/app/docs/api/common/mobile.yml')
def mobile(mobile):
    current_app.logger.debug("我是 debug 级别")
    current_app.logger.info("我是 info 级别")
    current_app.logger.warning("我是 warning 级别")
    current_app.logger.error("我是 error 级别")
    current_app.logger.critical("我是 critical 级别")

    try:
        1/0
    except ZeroDivisionError as e:
        current_app.logger.error(e)
    except Exception as e:
        current_app.logger("未知原因报错")


    return '愿世界一切安好,程序永无BUG!!!' + mobile