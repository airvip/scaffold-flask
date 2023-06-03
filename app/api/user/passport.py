#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from app.api import bp
from flask import request, jsonify, current_app, session
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)
from app.util.response_code import RET
from app.model import UserModel
from app import db, redis_obj, constant
from sqlalchemy.exc import IntegrityError
import re
from flasgger import swag_from

@bp.route("/register", methods=['POST'])
@swag_from("/app/docs/api/user/register.yml")
def register():
    req_dict = request.get_json()
    # print(req_dict)
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")
    username = req_dict.get("username")
    
    if not all([mobile, password, username]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数缺失")
    
    if not re.match(r"1[35789]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    userInfo = UserModel(username = username, mobile = mobile)
    # userInfo.generate_password_hash(password)
    userInfo.password = password
    try:
        db.session.add(userInfo)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error("mobile has exist, error: %s", e._message)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    session['username'] = mobile
    session['mobile'] = mobile
    session['id'] = userInfo.id

    return jsonify(errno=RET.OK, errmsg="注册成功")
    

@bp.route("/login", methods=['POST'])
@swag_from("/app/docs/api/user/login.yml")
def login():
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")
    
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数缺失")
    
    username = session.get("mobile")
    if username is not None:
        return jsonify(errno=RET.SESSIONERR, errmsg="该用户已登录")
    
    if not re.match(r"1[35789]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")
    
    user_ip = request.remote_addr
    try:
        access_num = redis_obj.get("access_num_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_num is not None and int(access_num) >= constant.LODIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多,请稍后重试")
    
    try:
        user = UserModel.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    if user is None or not user.check_password(password):
        try:
            redis_obj.incr("access_num_%s" % user_ip)
            redis_obj.expire("access_num_%s" % user_ip, constant.LODIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="账号或密码错误")
    
    session['username'] = user.username
    session['mobile'] = mobile
    session['user_id'] = user.id

    ret = {
        "access_token": create_access_token(identity=user.id),
        "refresh_token": create_refresh_token(identity=user.id)
    }
    return jsonify(errno=RET.OK, errmsg="登录成功", data=ret)


@bp.route("/session", methods=['GET'])
@swag_from("/app/docs/api/user/check_login.yml")
def check_login():
    mobile = session.get("mobile")
    if mobile is not None:
        return jsonify(errno=RET.OK, errmsg="用户已登录", data={"mobile":mobile})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")


@bp.route("/session", methods=["DELETE"])
@swag_from("/app/docs/api/user/logout.yml")
def logout():
    csrf_token = session.get("csrf_token")
    session.clear()
    session["csrf_token"] = csrf_token
    return jsonify(errno=RET.OK, errmsg="用户退出成功")


@bp.route('/refresh', methods=['POST'])
@swag_from("/app/docs/api/user/refresh.yml")
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret)

@bp.route('/jwtinfo', methods=['GET'])
@swag_from("/app/docs/api/user/jwtinfo.yml")
@jwt_required()
def jwtinfo():
    user_id = get_jwt_identity()
    username = UserModel.query.filter_by(id=user_id).first().username
    return jsonify(username=username)