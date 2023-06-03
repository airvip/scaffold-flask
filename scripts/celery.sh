#!/bin/bash
source ~/.bashrc
cd ~/workspace/python/scaffold-flask/
source .venv/bin/activate
exec celery -A app.tasks.main worker -l info

