#!/bin/bash
source ~/.bashrc
export FLASK_ENV=production
cd ~/workspace/python/scaffold-flask
# workon 进入虚拟环境只需要在后面加上虚拟环境名称
# workon .venv
source .venv/bin/activate
exec gunicorn -b 0.0.0.0:8889 --access-logfile ~/workspace/python/scaffold-flask/logs/access.log --error-logfile ~/workspace/python/scaffold-flask/logs/error.log main:app
