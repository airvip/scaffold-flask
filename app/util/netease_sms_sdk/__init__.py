#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import requests
import hashlib
import time
import uuid
import random
from . import config

class NeteaseSmsApi(object):
    """
    @description : 云信发送短信类
    """
    
    # 开发者平台分配的AppKey
    APP_KEY = config.APP_KEY
    # 开发者平台分配的AppSecret,可刷新
    APP_SECRET = config.APP_KEY

     # 接口列表:
    API_URLS = {
        "send": "https://api.netease.im/sms/sendcode.action",
        "verify": "https://api.netease.im/sms/verifycode.action",
        "send_template": "https://api.netease.im/sms/sendtemplate.action",
        "query_status": "https://api.netease.im/sms/querystatus.action",
    }

    def __init__(self, app_key=None, app_secret=None):
        self.app_key = app_key or self.APP_KEY
        self.app_secret = app_secret or self.APP_SECRET
        self.urls = self.API_URLS

    # 随机数（最大长度128个字符）
    @property
    def nonce(self):
        return uuid.uuid4().hex

    # 当前UTC时间戳，从1970年1月1日0点0 分0 秒开始到现在的秒数(String)
    @property
    def curtime(self):
        return str(int(time.time()))

    # SHA1(AppSecret + Nonce + CurTime),三个参数拼接的字符串，进行SHA1哈希计算，转化成16进制字符(String，小写)
    def checksum(self, nonce, curtime):
        s = "{}{}{}".format(self.app_secret, nonce, curtime).encode(encoding="utf-8")
        return hashlib.sha1(s).hexdigest()

    @property
    def http_headers(self):
        """ 构造 HTTP 请求头
        
        :return: 
        """
        nonce = self.nonce
        curtime = self.curtime
        checksum = self.checksum(nonce, curtime)

        return {
            "AppKey": self.app_key,
            "CurTime": curtime,
            "Nonce": nonce,
            "CheckSum": checksum,
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

    

    @staticmethod
    def _post(url, data, headers):
        r = requests.post(url, data=data, headers=headers)
        print("url: {}\nHTTP-header: {}\nHTTP-data: {}".format(url, headers, data))
        print("\tstatus: {} \tresult: {}".format(r.status_code, r.content))
        return r.json() if r.status_code == 200 else {}

    def send_code(self, mobile):
        url = self.urls.get("send")
        data = {
            "mobile": str(mobile)
        }
        return self._post(url, data=data, headers=self.http_headers)

    def check_code(self, mobile, code):
        url = self.urls.get("verify")
        data = {
            "mobile": str(mobile),
            "code": str(code)
        }
        return self._post(url, data=data, headers=self.http_headers)

    def send_template(self, template_id, mobiles, params=None):
        url = self.urls.get("send_template")
        data = {
            "mobiles": str([mobiles]) if not isinstance(mobiles, list) else mobiles
        }

        if template_id:
            data.update({"templateid": str(template_id)})

        if params:
            params = [params] if not isinstance(params, list) else params
            data.update({"params": str(params)})

        return self._post(url, data=data, headers=self.http_headers)

    def query_status(self, send_id):
        url = self.urls.get("query_status")
        data = {
            "sendid": str(send_id)
        }
        return self._post(url, data=data, headers=self.http_headers)