#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件 :verify_code.py
@说明 :
@时间 :2020/11/26 15:27:22
@作者 :airvip
'''

from app.api import bp
from app.util.captcha import Captcha
# from app.util.netease_sms_sdk import NeteaseSmsApi as sms
from app.util.tencent_sms_sdk import TencentSmsApi as sms
from app.util.response_code import RET
from io import BytesIO
from app import redis_obj, constant, db
from flask import current_app, jsonify, make_response, request
from app.model import UserModel
from app.tasks.sms.tasks import send_code, send_temp
from flasgger import swag_from


@bp.route("/sms")
@swag_from("/app/docs/api/common/sms.yml")
def send_template():
    # api = sms()
    # res = api.send_template('1599958', '13108765051', ["198642"])
    # res = api.send_template('1629709', '13108765051')
    # return res, 200, {"Content-type": "application/json"}
    # api = sms()
    # api.send_template(14891217, '13108765051', ["airvip", "阿尔维奇"])
    send_temp.delay('1599958', '13108765051', ["199212"])
    return '{"msg":"send template"}', 200, {"Content-type": "application/json"}

# GET /api/v1.0/image_code/<image_code_id>
@bp.route("/image_code/<image_code_id>")
@swag_from("/app/docs/api/common/get_image_code.yml")
def get_image_code(image_code_id):
    """
    @description :获取图片验证码
    ---------
    @param image_code_id: 图片验证码编号
    -------
    @Returns :
    -------
    """
    text, image = Captcha.gene_graph_captcha()
    # 存入redis,并设置有效期
    # redis_obj.set("image_code_%s" % image_code_id, text)
    # redis_obj.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
    try:
        redis_obj.setex("image_code_%s" % image_code_id, constant.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片验证码信息失败")
    
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.headers["Content-Type"] = "image/png"
    return resp


@bp.route("/sms_code/<re(r'1[3-9]\d{9}'):mobile>")
@swag_from('/app/docs/api/common/get_sms_code.yml')
def get_sms_code(mobile):
    # 参数接收
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")
    # 参数校验
    if not all([image_code, image_code_id]):
        return jsonify(errno=RET.PArAMERR, errmsg="参数错误")

    try:
        image_code_redis = redis_obj.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取图片验证码信息失败")

    if image_code_redis is None:
        return jsonify(errno=RET.NODATA, errmsg="验证码失效")
    
    # print(image_code_redis.lower())
    # print(image_code.lower())
    if str(image_code_redis.lower(), encoding=constant.ENCODING) != image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="验证码错误")

    try:
        user = UserModel.query.filter_by(mobile=mobile+1).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            return jsonify(errno=RET.DBERR, errmsg="相同手机号用户已存在")

    # 同步发送
    '''
    try:
        api = sms()
        ret = api.send_code(mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg=api['code'])
    '''
    # 使用 celery 异步发送code
    send_code.delay(mobile)

    # 需要后期使用云信的验证接口
    return jsonify(errno=RET.OK, errmsg="发送成功")