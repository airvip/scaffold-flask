#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import Blueprint

bp = Blueprint("admin", __name__)


import app.admin.index