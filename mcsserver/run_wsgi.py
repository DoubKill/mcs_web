import argparse
import logging
import os
import signal
import sys
import multiprocessing

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from gunicorn.app.base import BaseApplication

from basics.management.tasks.collect_wcs_data import collect_basket_num, collect_stock_info
from basics.management.tasks.env_check import check_env_task
from basics.management.tasks.mcs_dispatch import mcs_dispatch
from basics.management.tasks.send_order import send_order
from basics.management.tasks.stock_info import get_stock_info
from basics.management.tasks.sync_location import sync_locations
from mcs import settings
from mcs.wsgi import application as django_app
logger = logging.getLogger('apscheduler_log')


class DjangoApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application


def sig_handler(signum, frame):
    sys.exit(0)


def job_listener(event):
    job_id = event.job_id
    if event.exception:
        logger.error('作业ID:{},执行失败，错误原因：{}'.format(job_id, event.traceback))
    else:
        logger.info('作业ID:{},照常运行...'.format(job_id))


if __name__ == '__main__':
    try:
        signal.signal(signal.SIGTERM, sig_handler)  # kill pid
        signal.signal(signal.SIGINT, sig_handler)  # ctrl -c
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', "--port", type=int, default=9528, help='set app bind port')
        parser.add_argument('-s', "--settings", type=str, default='mcs.settings', help='set project config file')
        parser.add_argument('-w', "--workers", type=int, default=multiprocessing.cpu_count(),
                            help='number of Gunicorn worker processes')
        args = parser.parse_args()
        os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
        port = args.port
        print(f'Port={port}, Setting={args.settings}')
        worker_cnt = args.workers
        if worker_cnt >= 8:
            worker_cnt = 8

        options = {
            'bind': f'0.0.0.0:{port}',
            'workers': worker_cnt,
        }
        # 启动定时任务
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE, daemon=True)
        scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        scheduler.add_job(func=collect_basket_num,
                          trigger='cron',
                          second='*/3',
                          id='collect-basket-num',
                          max_instances=1,
                          replace_existing=True)
        scheduler.add_job(func=collect_stock_info,
                          trigger='cron',
                          second='*/10',
                          id='collect-stock-info',
                          max_instances=1,
                          replace_existing=True)
        scheduler.add_job(func=sync_locations,
                          trigger='cron',
                          minute='*/10',
                          id='sync-locations',
                          max_instances=1,
                          replace_existing=True)
        scheduler.add_job(func=get_stock_info,
                          trigger='cron',
                          minute='*/10',
                          id='stock-info',
                          max_instances=1,
                          replace_existing=True)
        # scheduler.add_job(func=check_env_task,
        #                   trigger='cron',
        #                   minute='*/1',
        #                   id='env_check',
        #                   max_instances=1,
        #                   replace_existing=True)
        scheduler.add_job(func=mcs_dispatch().run,
                          trigger='cron',
                          second='*/1',
                          id='mcs_dispatch',
                          max_instances=1,
                          replace_existing=True)
        scheduler.add_job(func=send_order().run,
                          trigger='cron',
                          second='*/1',
                          id='send_order',
                          max_instances=1,
                          replace_existing=True)
        scheduler.start()
        # 启动django服务
        DjangoApplication(django_app, options).run()

    except Exception as err:
        print(err)
