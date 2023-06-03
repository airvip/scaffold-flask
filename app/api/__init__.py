#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import Blueprint

bp = Blueprint("api", __name__)

import app.api.common
import app.api.user
import app.api.pay