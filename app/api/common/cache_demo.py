#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from app import cache
from app.api import bp
from flask import g, current_app
from flasgger import swag_from


@bp.route('/cache1')
@swag_from('/app/docs/api/common/cache1.yml')
def cache1():
    username = 'airvip'
    cache.set("username", username, timeout=30)
    # print(cache.get('username'))
    return cache.get('username') + '\n'

@bp.route('/cache2')
@swag_from('/app/docs/api/common/cache2.yml')
@cache.cached(timeout=50)
def cache2():
    return "你好 \n", 200, {"Content-Type": "application/text"}