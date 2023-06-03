#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@文件 :main.py
@说明 :
@时间 :2021/01/14 16:24:01
@作者 :airvip
'''

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR))

""" 
1. 创建一个 apscheduler 调度器对象
2. 配置调度器对象使用的  任务存储后端  执行器（线程，进程）
3. 添加定时任务
4. 启动 apscheduler 调度器对象 
"""

# 2
executors = {
    # 表示默认到了时间，该执行的定时任务都是放到进程池中的一个子进程执行
    # 5 表示进程池中最多有 5 个进程（同一时刻最多有 5 个进程同时执行）
    'default': ProcessPoolExecutor(5)
}

# 1 Blocking 阻塞的调度
scheduler = BlockingScheduler(executors=executors)

from compute import fix_compute_follows
from compute import get_schedule,get_schedule_day
# scheduler.add_job(fix_compute_follows, 'interval', seconds=10)
# scheduler.add_job(get_schedule, 'interval', seconds=30)
scheduler.add_job(get_schedule_day, 'cron', hour=16, minute=25)
# scheduler.add_job(get_schedule_day, 'interval', seconds=2)
# scheduler.add_job(get_schedule_day,'interval', seconds=2, misfire_grace_time=3600, max_instances=4)

if __name__ == '__main__':
    # 4 start()会阻塞当前文件退出
    scheduler.start()
    # get_schedule()

