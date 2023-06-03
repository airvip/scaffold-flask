#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import Blueprint, current_app, make_response
from flask_wtf import csrf

html = Blueprint("web_html", __name__)

@html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    """
    @description : 提供 html
    """
    if not html_file_name:
        html_file_name = "index.html"
    
    if html_file_name != "favicon.ico":
        html_file_name = "html/"+html_file_name

    # 创建一个 csrf_token 的值
    csrf_token = csrf.generate_csrf()

    # flask 提供的返回静态文件的方法
    resp = make_response(current_app.send_static_file(html_file_name)) 

    # 设置 cookie 值
    resp.set_cookie("csrf_token",csrf_token)
    return resp

