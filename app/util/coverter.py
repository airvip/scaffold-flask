#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from werkzeug.routing import BaseConverter

# 自定义转换器
class ReCoverter(BaseConverter):
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReCoverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex