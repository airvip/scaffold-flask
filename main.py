#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from app import create_app, db
from flask_migrate import Migrate
from flasgger import Swagger

from app.model import UserModel,RoleModel,user_role

# 开发模式创建应用
app = create_app("dev")

swagger_template = {"securityDefinitions": {"bearerAuth": {"type": "apiKey", "name": "Authorization", "in": "header"}}}
swagger = Swagger(app, template=swagger_template)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
