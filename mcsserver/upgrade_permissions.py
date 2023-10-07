import os
import sys

import django


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcs.settings")
django.setup()


from init_data import ps_data, method_dict, global_conf_data
from user.models import Permissions
from basics.models import Configuration


def up_perms():
    pp_code_list = []
    for item in ps_data:
        pm_code = item['code']
        child_perms = item.pop('operations', [])
        pp_code_list.append(pm_code)
        pp = Permissions.objects.filter(code=pm_code).first()
        if pp:
            cp_code_list = []
            Permissions.objects.filter(code=pm_code).update(**item)
            for c in child_perms:
                cp_code = '{}_{}'.format(c, pm_code)
                kwargs = {'code': cp_code}
                cp_data = {'name': method_dict[c], 'parent': pp}
                Permissions.objects.update_or_create(defaults=cp_data, **kwargs)
                cp_code_list.append(cp_code)
            pp.children_permissions.exclude(code__in=cp_code_list).delete()
        else:
            pp = Permissions.objects.create(**item)
            for c in child_perms:
                cp_data = {'code': '{}_{}'.format(c, pm_code), 'name': method_dict[c], 'parent': pp}
                Permissions.objects.create(**cp_data)
    Permissions.objects.filter(parent__isnull=True).exclude(code__in=pp_code_list).delete()

    for item in global_conf_data:
        if not Configuration.objects.filter(key=item['key']).exists():
            Configuration.objects.create(**item)


if __name__ == '__main__':
    up_perms()
