#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# 图片验证码的 redis 有效期， 单位：s
IMAGE_CODE_REDIS_EXPIRES = 600

# 自己编码
ENCODING = "utf-8"

# 登录错误尝试次数
LODIN_ERROR_MAX_TIMES = 5

# 登录错误限制时间，单位：s
LODIN_ERROR_FORBID_TIME = 86400

# 阿里云公网域名
OSS_WEB_DOMAIN = "https://dytapp.oss-cn-beijing.aliyuncs.com/"

# 缓存通用时间
REDIS_CACHE_COMMON_TIME = 7200

# 支付宝的网关地址（支付地址域名）
ALIPAY_URL_PREFIX = "https://openapi.alipaydev.com/gateway.do?"