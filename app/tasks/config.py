#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/2"