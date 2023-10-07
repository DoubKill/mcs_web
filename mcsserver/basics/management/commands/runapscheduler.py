# runapscheduler.py

import logging
import time

from django.core.management.base import BaseCommand

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from basics.management.tasks.collect_wcs_data import collect_basket_num, collect_stock_info
from basics.management.tasks.mcs_dispatch import mcs_dispatch
from basics.management.tasks.send_order import send_order
from basics.management.tasks.sync_location import sync_locations
from mcs import settings

logger = logging.getLogger('apscheduler_log')


def job_listener(event):
    job_id = event.job_id
    # scheduled_run_time = event.scheduled_run_time.strftime("%Y-%m-%d %H:%M:%S")
    if event.exception:
        logger.error('作业ID:{},执行失败，错误原因：{}'.format(job_id, event.traceback))
    else:
        logger.info('作业ID:{},照常运行...'.format(job_id))


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE, daemon=False)
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
        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
        except Exception:
            raise
