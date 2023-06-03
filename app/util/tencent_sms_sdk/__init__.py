#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from . import config

from tencentcloud.common import credential
# 导入对应产品模块的client models。
from tencentcloud.sms.v20210111 import sms_client, models
# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

class TencentSmsApi(object):
    """
    @description : 腾讯发送短信类
    """

    SECRET_ID = config.SecretId
    SECRET_KEY = config.SecretKey
    REGION = "ap-guangzhou"
    APP_ID = config.SmsSdkAppId
    SIGN_NAME = config.SignName


    def __init__(self, secret_id=None, secret_key=None):
        self.secret_id = secret_id or self.SECRET_ID
        self.secret_key = secret_key or self.SECRET_KEY

    # @property
    # def secretId(self):
    #     return self.secret_id

    # @property
    # def secretKey(self):
    #     return self.secret_key

    @staticmethod
    def gen_client(secret_id=None, secret_key=None, region=None):
        cred = credential.Credential(secret_id, secret_key)
        # print(cred.__dict__)

        # 实例化一个http选项，可选的，没有特殊需求可以跳过。
        httpProfile = HttpProfile()
        # 如果需要指定proxy访问接口，可以按照如下方式初始化hp
        # httpProfile = HttpProfile(proxy="http://用户名:密码@代理IP:代理端口")
        httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
        httpProfile.reqTimeout = 30    # 请求超时时间，单位为秒(默认60秒)
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

        # 非必要步骤:
        # 实例化一个客户端配置对象，可以指定超时时间等配置
        clientProfile = ClientProfile()
        # clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        # clientProfile.language = "en-US"
        clientProfile.httpProfile = httpProfile

        return sms_client.SmsClient(cred, region, clientProfile)


    def send_code(self, mobile):
        pass

    def send_template(self, template_id, mobiles, params=None):
        # 实例化一个请求对象，根据调用的接口和实际情况，可以进一步设置请求参数
        # 你可以直接查询SDK源码确定SendSmsRequest有哪些属性可以设置
        # 属性可能是基本类型，也可能引用了另一个数据结构
        # 推荐使用IDE进行开发，可以方便的跳转查阅各个接口和数据结构的文档说明
        req = models.SendSmsRequest()
        # 短信应用ID: 短信SdkAppId在 [短信控制台] 添加应用后生成的实际SdkAppId，示例如1400006666
        # 应用 ID 可前往 [短信控制台](https://console.cloud.tencent.com/smsv2/app-manage) 查看
        req.SmsSdkAppId = self.APP_ID
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名
        # 签名信息可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-sign) 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-sign) 的签名管理查看
        req.SignName = "滇医通"
        # 模板 ID: 必须填写已审核通过的模板 ID
        # 模板 ID 可前往 [国内短信](https://console.cloud.tencent.com/smsv2/csms-template) 或 [国际/港澳台短信](https://console.cloud.tencent.com/smsv2/isms-template) 的正文模板管理查看
        req.TemplateId = str(template_id)
        # 模板参数: 模板参数的个数需要与 TemplateId 对应模板的变量个数保持一致，，若无模板参数，则设置为空
        if params:
            req.TemplateParamSet = [params] if not isinstance(params, list) else params
        # req.TemplateParamSet = ["1234"]
        # 下发手机号码，采用 E.164 标准，+[国家或地区码][手机号]
        # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
        send_mobiles = []
        if not isinstance(mobiles, list):
            send_mobiles = ["+86"+mobiles]
        else:
            for mobile in mobiles:
                send_mobiles.append("+86"+mobile)
        req.PhoneNumberSet = send_mobiles
        # 用户的 session 内容（无需要可忽略）: 可以携带用户侧 ID 等上下文信息，server 会原样返回
        req.SessionContext = None
        # 短信码号扩展号（无需要可忽略）: 默认未开通，如需开通请联系 [腾讯云短信小助手]
        req.ExtendCode = None
        # 国内短信无需填写该项；国际/港澳台短信已申请独立 SenderId 需要填写该字段，默认使用公共 SenderId，无需填写该字段。注：月度使用量达到指定量级可申请独立 SenderId 使用，详情请联系 [腾讯云短信小助手](https://cloud.tencent.com/document/product/382/3773#.E6.8A.80.E6.9C.AF.E4.BA.A4.E6.B5.81)。
        req.SenderId = None
       

        # return req._serialize()
        client = self.gen_client(self.secret_id, self.secret_key, self.REGION)
        resp = client.SendSms(req)

        # 输出json格式的字符串回包
        # return resp.to_json_string()
        return resp.to_json_string() if resp.RequestId else {}
        # print(resp.to_json_string(indent=2))