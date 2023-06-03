#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from app.api import bp
from flask import jsonify, request
from app.util.login_check import login_required
from app.util.response_code import RET
from app import constant
from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig
import os

@bp.route("/orders/<int:order_id>/payment", methods=["POST"])
@login_required
def order_pay(order):
    
    # 参数获取校验


    # 支付宝网页下载的证书不能直接被使用，需要加上头尾
    # 你可以在此处找到例子： tests/certs/ali/ali_private_key.pem
    app_private_key_string = open(os.path.join(os.path.dirname(__file__), "keys/ali/app_private_key.pem")).read()
    alipay_public_key_string = open(os.path.join(os.path.dirname(__file__), "keys/ali/alipay_public_key.pem")).read()


    # 创建支付宝sdk的对象工具
    alipay = AliPay(
        appid="",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,而是你的公钥
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False,  # 默认False
        verbose=False,  # 默认False
        config=AliPayConfig(timeout=15)
    )
        
    

    # 手机网站支付 alipay.trade.wap.pay
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no="20161112",  # 订单编号
        total_amount=0.01,    # 订单金额
        subject=u"一件衣服",    # 主题  标题
        return_url="https://example.com",
        notify_url=None # 可选, 不填则使用默认notify url
        )

    # 构建让用户跳转的支付地址
    pay_url = constant.ALIPAY_URL_PREFIX + order_string
    return jsonify(errno=RET.OK, errmsg="OK", data={"pay_url": pay_url})



@bp.route("/order/payment", methods=["PUT"])
def save_order_payment_result():
    data = request.form.to_dict()
    # sign 不能参与签名验证
    signature = data.pop("sign")


    # 支付宝网页下载的证书不能直接被使用，需要加上头尾
    # 你可以在此处找到例子： tests/certs/ali/ali_private_key.pem
    app_private_key_string = open(os.path.join(os.path.dirname(__file__), "keys/ali/app_private_key.pem")).read()
    alipay_public_key_string = open(os.path.join(os.path.dirname(__file__), "keys/ali/alipay_public_key.pem")).read()


    # 创建支付宝sdk的对象工具
    alipay = AliPay(
        appid="",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,而是你的公钥
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False,  # 默认False
        verbose=False,  # 默认False
        config=AliPayConfig(timeout=15)
    )

    # verify
    success = alipay.verify(data, signature)
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED" ):
        # 修改订单数据
        print("trade succeed")
