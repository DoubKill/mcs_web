# 同步休息位至RCS，全量同步

import logging
import os

import django
import requests


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcs.settings")
django.setup()

from basics.models import Location, LocationGroupRelation, PlatFormInfo, Configuration

send_log = logging.getLogger('api_log')


def rest_location_push(rcs_url, data):
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    try:
        url = rcs_url + '/api/dispatch/universal/basic-data/locations/group_status/'
        response = requests.post(url, json={'data': data}, headers=headers, timeout=5)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        send_log.error('休息位推送失败，info:{}'.format(e))
        return False
    else:
        send_log.info('休息位推送成功，info:{}'.format(response.text))
        return True


def sync_locations():
    data = []
    locations = Location.objects.all()
    rcs_url = Configuration.objects.get(key='rcs_url').value
    if locations and rcs_url:

        for location in locations:
            location_data = {
                'location_name': location.location_name,
                'fit_group': [],
                'if_relay': False,
                'if_active': location.is_used
            }
            location_group_relations = LocationGroupRelation.objects.filter(location=location)
            for relation in location_group_relations:
                platform_infos = PlatFormInfo.objects.filter(location_group=relation.location_group).all()

                if platform_infos:
                    for platform_info in platform_infos:
                        platform_data = {
                            'machine_no': platform_info.platform_ID,
                            'priority': relation.priority
                        }
                        location_data['fit_group'].append(platform_data)
            data.append(location_data)

        send_log.info('开始推送休息位：{}'.format(','.join(list(locations.values_list('location_name', flat=True)))))
        success_flag = rest_location_push(rcs_url, data)


if __name__ == '__main__':
    sync_locations()
