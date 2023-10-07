# db_init.py:项目初始化运行


import os

from django.core.management.base import BaseCommand

from init_data import init_permissions, init_global_conf
from user.models import User, Department


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('开始迁移数据库')
        apps = ('agv', 'basics', 'monitor', 'openapi', 'user')
        #
        # os.system(
        #     './manage makemigrations {}'.format(
        #         ' '.join(apps)
        #     ))
        os.system('./manage migrate')
        os.system('./manage collectstatic --noinput')

        print('创建超级管理员...')
        User.objects.create_superuser('gzmcs123', '123456@qq.com', '123456')
        Department.objects.create(name='浙江国自机器人技术股份有限公司')
        init_permissions()
        init_global_conf()