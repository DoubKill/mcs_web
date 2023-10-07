# db_init.py:项目初始化运行
from django.core.management import BaseCommand

from upgrade_permissions import up_perms


class Command(BaseCommand):

    def handle(self, *args, **options):
        up_perms()