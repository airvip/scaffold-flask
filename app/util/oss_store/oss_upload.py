#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# -*- coding: utf-8 -*-
from __future__ import print_function
import os, sys
import oss2
import uuid
from . import config


def storage(file_data, suffix = None):
    """
    @description : 文件上传
    ---------
    @param suffix : hello.py的后缀名  例如： .py
    -------
    @Returns :
    -------
    """
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(config.AccessKey, config.AccessSecret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, config.EndPoint, config.BucketName)
    # 当无法确定待上传的数据长度时，total_bytes的值为None。
    def percentage(consumed_bytes, total_bytes):
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print('\r{0}% '.format(rate), end='')
            sys.stdout.flush()

    # 后缀名必须填写
    if suffix == None:
        suffix = ''
    else:
        suffix = suffix 

    filename = str(uuid.uuid1()) + suffix

    # progress_callback为可选参数，用于实现进度条功能。
    result = bucket.put_object(filename, file_data, progress_callback=percentage)
    # print(result.__dict__.items())
    # print('\n'.join(['%s:%s' % item for item in result.__dict__.items()]))
    """
    resp:<oss2.http.Response object at 0x7f2e439e9c88>
    status:200
    headers:{'Server': 'AliyunOSS', 'Date': 'Tue, 08 Dec 2020 09:06:58 GMT', 'Content-Length': '0', 'Connection': 'keep-alive', 'x-oss-request-id': '5FCF4232BDB66C31367C8728', 'ETag': '"610647EE01F7676B4BA3C9F7B4044B31"', 'x-oss-hash-crc64ecma': '14395357795886080751', 'Content-MD5': 'YQZH7gH3Z2tLo8n3tARLMQ==', 'x-oss-server-time': '41'}
    request_id:5FCF4232BDB66C31367C8728
    versionid:None
    delete_marker:None
    etag:610647EE01F7676B4BA3C9F7B4044B31
    crc:14395357795886080751
    """
    # print(result.status)
    # print(type(result.status))
    if result.status == 200:
        return filename
    else:
        raise Exception("上传文件出错")
    


if __name__ == '__main__':
    with open('//root/workspace/python/scaffold-flask/app/static/favicon.ico', 'rb') as f:
        file_data = f.read()
        storage(file_data)