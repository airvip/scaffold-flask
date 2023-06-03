#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
import datetime,time
from . import BaseModel

from app import db
 
    
user_role = db.Table(
    "base_user_role",
    db.Column("user_id", db.BigInteger, db.ForeignKey("base_user.id"), primary_key=True, comment="用户id"),
    db.Column("role_id", db.BigInteger, db.ForeignKey("base_role.id"), primary_key=True, comment="角色id")
)

class UserModel(BaseModel, db.Model):
    """
    @description : 用户表模型类
    """
    __tablename__ = "base_user"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment="用户id") # 用户id
    username = db.Column(db.String(50), nullable=False,comment="用户名") # 用户名
    mobile = db.Column(db.String(11), nullable=False, unique=True, comment="手机号") # 手机号
    password_hash = db.Column(db.String(128), nullable=False, comment="密码") # 密码
    avatar_url = db.Column(db.String(255), nullable=False, default='', comment="头像") # 密码

    roles = db.relationship("RoleModel", secondary=user_role) # 角色信息

    # 添加 property 装饰器之后，会把函数变为属性，属性名即为函数名
    @property
    def password(self):
        """
        @description : 密码属性不可读
        """
        raise AttributeError("can't read")

    @password.setter
    def password(self, origin_password):
        """
        @description : 设置密码
        """
        self.password_hash = generate_password_hash(origin_password)

    def check_password(self, origin_password):
        """
        @description : 密码验证
        """
        return check_password_hash(self.password_hash, origin_password)

    def to_dict(self):
        """
        @description : 转换为字典
        """
        print(type(self.update_time))
        update_time = ""
        if self.update_time is not None:
            update_time = self.update_time.strftime("%Y-%m-%d %H:%M:%S")
            
        return {
            "user_id": self.id,
            "username": self.username,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": update_time # int(time.mktime(self.update_time.timetuple())) # 显示的时候记着+8小时
        }

    def auth_to_dict(self):
        """
        @description : 实名信息转字典(暂无实名信息如：身份证号)
        """
        pass

    

class RoleModel(BaseModel, db.Model):
    """
    @description : 角色模型
    """
    __tablename__ = "base_role"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment="角色id") # pk
    name = db.Column(db.String(50), nullable=False, unique=True, comment="角色名") # 名称

    users = db.relationship("UserModel", secondary=user_role) # 角色信息
    
    def to_dict(self):
        """
        @description : 转换为字典
        """
        update_time = ""
        if self.update_time is not None:
            update_time = self.update_time.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "role_id": self.id,
            "role_name": self.name,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": update_time
        }


