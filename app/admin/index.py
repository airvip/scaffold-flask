#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from app.admin import bp
from flask import render_template, current_app,__version__
import datetime


@bp.route('/', methods=['GET'])
def index():
    # print( url_for('static', filename='css/style.css') )
    now_date_time = datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S %f' )
    return render_template("admin/index.html", data = {'name':'Flask', 'version':__version__, 'now_date_time': now_date_time})
