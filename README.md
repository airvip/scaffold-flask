# 工作流

1. 编写 model 文件，方便数据管理
2. 编写接口文件 api 获取业务 

# 配置文件
1. app/config.py
2. app/util/xxxx/config.py

# swagger
`http://127.0.0.1:5000/apidocs/#/`

# 技术栈

* flask2.+
* Flask-SQLAlchemy
* Flask-Migrate
* pillow
* oss
* celery
* redis  也可以使用 Flask-Cache
* alipay 第三方非官方  https://github.com/fzlee/alipay/blob/master/README.md
* sms 网易云信 腾讯云
* jwt

## 开发阶段 python 虚拟环境
```
# 已安装的包
root@airvip:~# pip3 list --format=columns

# 通过 pip 安装 virtualenv
root@airvip:~# pip3 install virtualenv

# 测试安装
root@airvip:~# virtualenv --version

# 在项目中生成虚拟环境
root@airvip:~# virtualenv .venv

# Linux 系统 启用虚拟环境
root@airvip:~/workspace/python/scaffold-flask# source .venv/bin/activate

# 停用虚拟环境
(.venv) root@airvip:~/workspace/python/scaffold-flask# deactivate
```

### 项目以开发环境运行

```
(.venv) root@airvip:~/workspace/python/scaffold-flask# export -p
(.venv) root@airvip:~/workspace/python/scaffold-flask# export FLASK_ENV=development
(.venv) root@airvip:~/workspace/python/scaffold-flask# export FLASK_APP=main.py
(.venv) root@airvip:~/workspace/python/scaffold-flask# flask run --host=0.0.0.0
```


### 开发完成，生成 requirements.txt 依赖文件
```
# 查看当前安装依赖包版本
pip freeze
# 依赖包生成 requirements.txt
pip freeze > requirements.txt
```

### 新环境部署，安装 requirements.txt 依赖

```
pip install -r requirements.txt
```

### 数据表迁移

```
python main.py db init
python main.py db migrate -m 'init tables'
# 执行了该语句数据库才会有表创建
python main.py db upgrade  


flask db init
flask db migrate -m 'init tables'
# 执行了该语句数据库才会有表
flask db upgrade
```

# 阿里云 OSS

```
https://help.aliyun.com/document_detail/85288.html?spm=a2c4g.32025.0.0.3cb578d4lJP7Oc
apt-get install python-dev -y
pip install oss2
```

# celery 启动, 
```
# 如果只是一个单文件
(.venv) root@airvip:~/workspace/python/scaffold-flask# celery -A app.tasks.task_sms worker -l info

# 如果是按照包的形式
(.venv) root@airvip:~/workspace/python/scaffold-flask# celery -A app.tasks.main worker -l info
```


# 项目运行脚本
```
scripts# tree
.
├── celery.sh
└── main.sh
```

# 目录结构
```
scaffold-flask# tree
.
├── README.md
├── app
│   ├── __init__.py
│   ├── admin
│   │   ├── __init__.py
│   │   └── index.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── common
│   │   │   ├── __init__.py
│   │   │   ├── cache_demo.py
│   │   │   ├── ping.py
│   │   │   └── verify_code.py
│   │   ├── pay
│   │   │   ├── __init__.py
│   │   │   ├── ali_pay.py
│   │   │   └── keys
│   │   │       ├── README.md
│   │   │       └── ali
│   │   │           ├── alipay_public_key.pem
│   │   │           ├── app_private_key.pem
│   │   │           └── app_public_key.pem
│   │   └── user
│   │       ├── __init__.py
│   │       ├── passport.py
│   │       └── user.py
│   ├── config.py
│   ├── constant.py
│   ├── docs   #### swagger 文档目录
│   │   └── api
│   │       ├── common
│   │       │   ├── cache1.yml
│   │       │   ├── cache2.yml
│   │       │   ├── get_image_code.yml
│   │       │   ├── get_sms_code.yml
│   │       │   ├── mobile.yml
│   │       │   ├── ping.yml
│   │       │   └── sms.yml
│   │       └── user
│   │           ├── check_login.yml
│   │           ├── get_user_list.yml
│   │           ├── jwtinfo.yml
│   │           ├── login.yml
│   │           ├── logout.yml
│   │           ├── refresh.yml
│   │           ├── register.yml
│   │           └── set_user_avatar.yml
│   ├── html.py
│   ├── model
│   │   ├── __init__.py
│   │   └── user_role.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   ├── favicon.ico
│   │   ├── html
│   │   │   └── index.html
│   │   ├── img
│   │   │   └── README.md
│   │   └── js
│   │       └── hello.js
│   ├── tasks
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── sms
│   │   │   ├── __init__.py
│   │   │   └── tasks.py
│   │   └── task_sms.py
│   ├── templates
│   │   └── admin
│   │       ├── base.html
│   │       └── index.html
│   └── util
│       ├── captcha
│       │   ├── CascadiaCodePL.ttf
│       │   ├── Courgette Regular.ttf
│       │   └── __init__.py
│       ├── coverter.py
│       ├── login_check.py
│       ├── netease_sms_sdk
│       │   ├── __init__.py
│       │   └── config.py
│       ├── oss_store
│       │   ├── config.py
│       │   └── oss_upload.py
│       ├── response_code.py
│       └── tencent_sms_sdk
│           ├── __init__.py
│           └── config.py
├── favicon.ico
├── logs
│   └── README.md
├── main.py
├── migrations  #### 自动创建的
│   └── README
├── requirements.txt
├── schedule
│   ├── __init__.py
│   ├── compute.py
│   └── main.py
└── scripts
    ├── celery.sh
    └── main.sh
```