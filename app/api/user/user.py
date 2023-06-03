#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from app.api import bp
from app.util.login_check import login_required
from app.util.response_code import RET
from app.util.oss_store.oss_upload import storage
from flask import current_app, request, g, jsonify
import os, json
from flasgger import swag_from

from app.model import UserModel
from app import db, redis_obj
from app.constant import OSS_WEB_DOMAIN, REDIS_CACHE_COMMON_TIME

@bp.route("/user/avatar", methods=["POST"])
@login_required
@swag_from("/app/docs/api/user/set_user_avatar.yml")
def set_user_avatar():
    """
    @description :设置用户头像
    ---------
    @param avatar: 图片(多媒体表单格式)
    @param id: 用户id g.user_id
    -------
    @Returns :
    -------
    """
    image = request.files.get("avatar")

    if image is None:
        return jsonify(errno=RET.PARAMERR, errmsg="未上传图片")

    suffix = os.path.splitext(image.filename)[-1]
    # 调用oss上传
    try:
        file_name_url = storage(image.read(), suffix=suffix)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传失败")
    # print("头像名称是：" + file_name_url)
    # 将头像路径保存到数据库
    user_id = g.user_id
    try:
        UserModel.query.filter_by(id=user_id).update({"avatar_url":file_name_url})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")
    
    return jsonify(errno=RET.OK, errmsg="上传成功", data={"avatar_url":OSS_WEB_DOMAIN + file_name_url})
    

@bp.route("/user", methods=["GET"])
@login_required
@swag_from("/app/docs/api/user/get_user_list.yml")
def get_user_list():
    # 尝试从 redis 中获取数据
    try:
        resp_json = redis_obj.get("all_user_list")
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json is not None:
            return resp_json, 200, {"Content-Type": "application/json"}
   
    # 查询数据库
    try:
        user_obj =  db.session.execute(db.select(UserModel).order_by(UserModel.create_time.desc())).scalars()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")
    
    user_list = []
    for user in user_obj:
        user_list.append(user.to_dict())

    # 将数据转换为字典字符串
    resp_dict = dict(errno=RET.OK, errmsg="获取成功", data=user_list)
    resp_json = json.dumps(resp_dict)

    try:
        redis_obj.setex("all_user_list", REDIS_CACHE_COMMON_TIME, resp_json)
    except Exception as e:
        current_app.logger.error(e)

    return resp_json, 200, {"Content-Type": "application/json"}