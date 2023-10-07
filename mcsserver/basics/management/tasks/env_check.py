# 下发环境车检测任务

import json
import logging
import os
import datetime

import django
import requests


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcs.settings")
django.setup()

from agv.models import EnvCheckTasks, EnvLocationCheckHistory, EnvTaskLocationRelation
from basics.models import Configuration

collect_logger = logging.getLogger('collect_log')


def issue_task(rcs_url, check_no, location_names):
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    parameters = json.dumps({"check_no": check_no, "location_list": ','.join(location_names)})
    order_json = {
        "order_name": check_no,
        "priority": 0,
        "dead_line": datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S'),
        "ts_name": 'env_order',
        "parameters": parameters
    }

    try:
        url = rcs_url + '/api/om/order/'
        response = requests.request("POST", url, json=order_json, headers=headers, timeout=3)
    except Exception as e:
        return False
    if response.status_code == 200:
        return True
    return False


def create_task(check_no, task_no, working_area_name, location_names, state):
    for location_name in location_names:
        EnvLocationCheckHistory.objects.create(
            check_no=check_no,
            location_name=location_name,
            task_no=task_no,
            working_area_name=working_area_name,
            state=state,
            check_state=1,
        )


def check_env_task():
    now_time = datetime.datetime.now()
    rcs_url = Configuration.objects.get(key='rcs_url').value

    for t in EnvCheckTasks.objects.filter(is_used=True):
        if t.task_trigger_type == 1:  # 单次任务比对时间
            trigger_time = t.trigger_time[0][:16]
            if now_time.strftime('%Y-%m-%d %H:%M') == trigger_time:
                check_no = '{}{}'.format(t.task_no, now_time.strftime('%Y%m%d%H%M%S'))
                location_names = list(EnvTaskLocationRelation.objects.filter(
                    check_task=t).values_list('check_location__location_name', flat=True).order_by('ordering'))
                success_flag = issue_task(rcs_url, check_no, location_names)
                if success_flag:
                    state = 1
                else:
                    state = 0
                create_task(check_no, t.task_no, t.working_area.area_name, location_names, state)
        else:  # 每日任务，比对时间点
            trigger_times = t.trigger_time
            for i in trigger_times:
                if now_time.strftime('%H:%M') == i[:5]:
                    check_no = '{}{}'.format(t.task_no, now_time.strftime('%Y%m%d%H%M%S'))
                    location_names = list(EnvTaskLocationRelation.objects.filter(
                        check_task=t).values_list('check_location__location_name', flat=True).order_by('ordering'))
                    success_flag = issue_task(rcs_url, check_no, location_names)
                    if success_flag:
                        state = 1
                    else:
                        state = 0
                    create_task(check_no, t.task_no, t.working_area.area_name, location_names, state)


if __name__ == '__main__':
    check_env_task()