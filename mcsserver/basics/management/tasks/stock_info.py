# 定时插入堆栈和AGV小车在制汇总数据

import datetime
import logging
import os

import django
from django.db.models import Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcs.settings")
django.setup()

from basics.models import PlatformGroup
from monitor.models import StockHistorySummary
from monitor.utils import get_agv_info
from agv.models import CacheDeviceStock

stock_log = logging.getLogger('api_log')


def get_stock_info():
    """定时获取AGV实时在制"""
    data, code = get_agv_info()
    process_group_dict = dict(PlatformGroup.objects.values_list(
        'group_ID', 'process__process_name'))
    route_group_dict = dict(PlatformGroup.objects.values_list(
        'group_ID', 'route_schema__route_name'))
    ret = {}
    date_now = datetime.datetime.now()
    if code == 200 and "code" in data and data["code"] == 0:
        success_list = data["data"]['data']
        for item in success_list:
            g1_process_name = process_group_dict.get(item['G1A']['machine_group'])
            g1_route_name = route_group_dict.get(item['G1A']['machine_group'])
            g2_process_name = process_group_dict.get(item['G2A']['machine_group'])
            g2_route_name = route_group_dict.get(item['G2A']['machine_group'])
            if g1_process_name:
                k1 = '{}-{}'.format(g1_route_name, g1_process_name)
                if k1 not in ret:
                    ret[k1] = {'process_name': g1_process_name,
                               'route_name': g1_route_name, 'agv_trains_num': 1,
                               'created_time': date_now}
                else:
                    ret[k1]['agv_trains_num'] += 1
            if g2_process_name:
                k2 = '{}-{}'.format(g2_route_name, g2_process_name)
                if k2 not in ret:
                    ret[k2] = {'process_name': g2_process_name,
                               'route_name': g2_route_name, 'agv_trains_num': 1,
                               'created_time': date_now}
                else:
                    ret[k2]['agv_trains_num'] += 1
    else:
        stock_log.error('获取AGV在制失败！')

    # 补充堆栈在制数据
    cache_stock_data = CacheDeviceStock.objects.values('in_material_type_name').annotate(cnt=Count('id'))
    for cs in cache_stock_data:
        c_group_ID = cs['in_material_type_name']
        cnt = cs['cnt']
        if c_group_ID:
            process_name = process_group_dict.get(c_group_ID)
            route_name = route_group_dict.get(c_group_ID)
            if process_name:
                ck = '{}-{}'.format(route_name, process_name)
                if ck not in ret:
                    ret[ck] = {'process_name': process_name,
                               'route_name': route_name,
                               'cache_trains_num': cnt,
                               'created_time': date_now}
                else:
                    if 'cache_trains_num' not in ret[ck]:
                        ret[ck]['cache_trains_num'] = cnt
                    else:
                        ret[ck]['cache_trains_num'] += cnt
    for stock_info in ret.values():
        StockHistorySummary.objects.create(**stock_info)


if __name__ == '__main__':
    get_stock_info()
