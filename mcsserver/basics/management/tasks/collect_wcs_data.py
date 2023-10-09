# 定时更新站台花篮数、上下料屏蔽等


import json
import logging
import os
import datetime
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import django
import requests


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcs.settings")
django.setup()

from basics.models import PlatFormRealInfo, CacheDeviceInfo, Configuration, PlatFormInfo
from agv.models import CacheDeviceStock
collect_logger = logging.getLogger('collect_log')


def request_wcs(wcs_url, device_name, inter_face_Name, control1=""):
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    req_data = {
        "Request": {
            "control1": control1,
            "deviceName": device_name,
            "deviceType": "opc_ua",
            "interfaceName": inter_face_Name,
            "subInterfaceId": ""
        }
    }
    all_content = []
    try:
        url = wcs_url + '/api/wcs/call_interface'
        resp = requests.request("POST", url, json=req_data, headers=headers, timeout=2)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        collect_logger.error('站台：{}, 点位：{}，请求超时！'.format(device_name, inter_face_Name))
    else:
        resp_json_data = resp.json()
        resp_data = resp_json_data['Response']
        if resp_data['Result'] == 'True':
            contents = resp_data['RecvData']
            if contents:
                for i in contents:
                    if not i['content']:
                        continue
                    all_content.extend(i['content'])
        else:
            collect_logger.error('站台：{}, 点位：{}，请求失败！'.format(device_name, inter_face_Name))
    return all_content


def request_wcs_fz(wcs_url, device_name, inter_face_Name, control1=""):
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    req_data = {
        "Request": {
            "control1": control1,
            "deviceName": device_name,
            "deviceType": "opc_ua",
            "interfaceName": inter_face_Name,
            "subInterfaceId": ""
        }
    }
    try:
        url = wcs_url + '/api/wcs/call_interface'
        resp = requests.request("POST", url, json=req_data, headers=headers, timeout=2)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        collect_logger.error('站台：{}, 点位：{}，请求超时！'.format(device_name, inter_face_Name))
        return None
    else:
        resp_json_data = resp.json()
        resp_data = resp_json_data['Response']
        if resp_data['Result'] == 'True':
            return resp_data['RecvData'][0]['content']
        collect_logger.error('站台：{}, 点位：{}，请求失败！'.format(device_name, inter_face_Name))
        return None


# 获取全部机台全部点位
def batch_request_wcs(wcs_url, device_names, inter_face_Name):
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    req_data = {
        "Request": {
            "control1": "",
            "deviceName": device_names,
            "deviceType": "opc_ua",
            "interfaceName": inter_face_Name,
            "subInterfaceId": ""
        }
    }
    try:
        url = wcs_url + '/api/wcs/get_devices_info'
        resp = requests.request("POST", url, json=req_data, headers=headers, timeout=5)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        collect_logger.error('WCS请求超时！')
        return {}
    else:
        resp_json_data = resp.json()
        return resp_json_data


# 同一机台点位全部获取
# def batch_request_wcs(plt, wcs_url, device_name, inter_face_Name):
#     headers = {
#         'Content-Type': "application/json",
#         'cache-control': "no-cache",
#         'charset': 'utf-8',
#     }
#     req_data = {
#         "Request": {
#             "control1": "",
#             "deviceName": device_name,
#             "deviceType": "opc_ua",
#             "interfaceName": inter_face_Name,
#             "subInterfaceId": ""
#         }
#     }
#     try:
#         url = wcs_url + '/api/wcs/call_interface'
#         resp = requests.request("POST", url, json=req_data, headers=headers, timeout=2)
#         resp.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         collect_logger.error('站台：{}, 点位：{}，请求超时！'.format(device_name, inter_face_Name))
#         return plt, False
#     else:
#         resp_json_data = resp.json()
#         resp_data = resp_json_data['Response']
#         if resp_data['Result'] == 'True':
#             ret = resp_data['RecvData'][0]['content'].split(',')
#             for idx, v in enumerate(ret):
#                 if idx == 0:
#                     if plt.upper_basket_num != v:
#                         plt.upper_basket_num = v
#                         plt.upper_basket_changed_time = datetime.datetime.now()
#                 elif idx == 1:
#                     if plt.lower_basket_num != v:
#                         plt.lower_basket_num = v
#                         plt.lower_basket_changed_time = datetime.datetime.now()
#                 elif idx == 2:
#                     plt.state = v
#                 elif idx == 3:
#                     plt.upper_rail_state = v
#                 elif idx == 4:
#                     plt.lower_rail_state = v
#                 plt.is_connected = True
#             return plt, True
#         else:
#             collect_logger.error('站台：{}, 点位：{}，请求失败！'.format(device_name, inter_face_Name))
#             plt.is_connected = False
#             return plt, False


def collect_stock_info():
    """定时获取堆栈库存"""
    in_location_names = dict(CacheDeviceInfo.objects.values_list('in_location_name', 'device_name'))
    wcs_url = Configuration.objects.get(key='wcs_url').value
    now_time = datetime.datetime.now()
    # 站台、工艺段关系
    station_process = dict(PlatFormInfo.objects.all().values_list('platform_ID', 'process__process_ID'))
    try:
        dz_fz_flag = int(Configuration.objects.get(key='dz_fz').value)
    except Exception:
        dz_fz_flag = 0
    for in_location_name, device_name in in_location_names.items():
        if dz_fz_flag:
            ret = request_wcs_fz(wcs_url, in_location_name, 'stock_inventory')
            try:
                ret_data = json.loads(ret)
            except Exception:
                CacheDeviceInfo.objects.filter(device_name=device_name).update(is_connected=False)
                continue
            for item in ret_data:
                row = item['row']
                column = item['column']
                layer = item['layer']
                kwargs = {'row': row, 'column': column, 'layer': layer, 'equip_code': device_name}
                if not item['material_out_time']:
                    output_time_consume, layoff_time, storge_time = None, None, 0
                else:
                    output_time_consume = item['material_out_time'] * 60
                    storge_time = item.get('storge_time', 0) * 60
                    layoff_time_instance = CacheDeviceStock.objects.filter(**kwargs).last()
                    layoff_time = layoff_time_instance.layoff_time if layoff_time_instance.layoff_time else (
                        (now_time - datetime.timedelta(seconds=output_time_consume + storge_time)).strftime(
                            '%Y-%m-%d %H:%M:%S'))
                defaults = {
                    'in_processID': item['process_id'],
                    'in_material_type_name': item['material_type'],
                    'equipID': item['equip_id'],
                    'output_time_consume': output_time_consume,
                    'storge_time': storge_time,
                    'q_time': item['Qtime'],
                    'in_task_no': item['in_order_id'],
                    'basket_num': item['deposit'],
                    'layoff_time': layoff_time
                }
                CacheDeviceStock.objects.filter(**kwargs).update(**defaults)
                CacheDeviceInfo.objects.filter(device_name=device_name).update(is_connected=True)
        else:
            ret_data = request_wcs(wcs_url, in_location_name, 'stock_inventory')
            if not ret_data:
                CacheDeviceInfo.objects.filter(device_name=device_name).update(is_connected=False)
                continue
            for item in ret_data:
                row = item['row']
                column = item['column']
                layer = item['layer']
                kwargs = {'row': row, 'column': column, 'layer': layer, 'equip_code': device_name}
                if not item['material_out_time']:
                    output_time_consume, layoff_time, storge_time = None, None, 0
                else:
                    output_time_consume = item['material_out_time'] * 60
                    storge_time = item.get('storge_time', 0) * 60
                    layoff_time_instance = CacheDeviceStock.objects.filter(**kwargs).last()
                    layoff_time = layoff_time_instance.layoff_time if layoff_time_instance.layoff_time else (
                        (now_time - datetime.timedelta(seconds=output_time_consume + storge_time)).strftime('%Y-%m-%d %H:%M:%S'))
                defaults = {
                    'in_processID': station_process.get(item['equip_id'], ''),
                    'in_material_type_name': item['material_type'],
                    'equipID': item['equip_id'],
                    'output_time_consume': output_time_consume,
                    'storge_time': storge_time,
                    'q_time': item['Qtime'],
                    'in_task_no': item['in_order_id'],
                    'basket_num': item['deposit'],
                    'layoff_time': layoff_time
                }
                CacheDeviceStock.objects.filter(**kwargs).update(**defaults)
                CacheDeviceInfo.objects.filter(device_name=device_name).update(is_connected=True)

#  单个点位获取
# def collect_basket_num():
#     """定时获取站台花篮数"""
#     plts = PlatFormRealInfo.objects.filter(
#         platform_info__is_used=True, platform_info__location_name__isnull=False).select_related('platform_info')
#     wcs_url = Configuration.objects.get(key='wcs_url').value
#     basket_updates = []
#     basket_update_ids = []
#     interfaceNames = ['GZ_EquipmentLoadCasNum', 'GZ_EquipmentUnloadCasNum', 'GZ_EquipmentProductionStatus',
#                       'GZ_EquipmentLoadDisable', 'GZ_EquipmentUnloadDisable']
#     if wcs_url:
#         for plt in plts:
#             device_name = plt.platform_info.location_name
#             all_task = []
#             with ThreadPoolExecutor(max_workers=6) as executor:
#                 for i in interfaceNames:
#                     all_task.append(executor.submit(request_wcs, wcs_url, device_name, i))
#                 # 主线程等待所有子线程完成
#                 wait(all_task, timeout=3, return_when=ALL_COMPLETED)
#                 success_flag = False
#                 for idx, i in enumerate(all_task):
#                     ret = i.result()
#                     if ret is not None:
#                         success_flag = True
#                         if idx == 0:
#                             if plt.upper_basket_num != ret:
#                                 plt.upper_basket_num = ret
#                                 plt.upper_basket_changed_time = datetime.datetime.now()
#                         elif idx == 1:
#                             if plt.lower_basket_num != ret:
#                                 plt.lower_basket_num = ret
#                                 plt.lower_basket_changed_time = datetime.datetime.now()
#                         elif idx == 2:
#                             plt.state = ret
#                         elif idx == 3:
#                             plt.upper_rail_state = ret
#                         elif idx == 4:
#                             plt.lower_rail_state = ret
#                         # elif idx == 5:
#                         #     plt.dock_status = 0 if not ret else ret
#                 if success_flag:
#                     # plt.last_updated_time = datetime.datetime.now()
#                     basket_updates.append(plt)
#                     basket_update_ids.append(plt.id)
#
#     # 批量更新
#     if basket_updates:
#         PlatFormRealInfo.objects.bulk_update(basket_updates, fields=[
#             'upper_basket_num', 'upper_basket_changed_time',
#             'lower_basket_num', 'lower_basket_changed_time',
#             'state', 'upper_rail_state', 'lower_rail_state'
#         ])
#         PlatFormRealInfo.objects.filter(id__in=basket_update_ids).update(last_updated_time=datetime.datetime.now())

#
# def collect_basket_num():
#     """定时获取站台花篮数"""
#     plts = PlatFormRealInfo.objects.filter(
#         platform_info__is_used=True, platform_info__location_name__isnull=False).select_related('platform_info')
#     wcs_url = Configuration.objects.get(key='wcs_url').value
#     basket_updates = []
#     basket_update_ids = []
#     plts.update(begin_time=datetime.datetime.now())
#     if wcs_url:
#         all_task = []
#         with ThreadPoolExecutor(max_workers=6) as executor:
#             for plt in plts:
#                 device_name = plt.platform_info.location_name
#                 all_task.append(executor.submit(batch_request_wcs, plt, wcs_url, device_name, 'GZ_AGVInfo'))
#             for tsk in all_task:
#                 ret = tsk.result()
#                 plt_instance, success_flag = ret[0], ret[1]
#                 basket_updates.append(plt_instance)
#                 if success_flag:
#                     basket_update_ids.append(plt_instance.id)
#     # 批量更新
#     if basket_updates:
#         PlatFormRealInfo.objects.bulk_update(basket_updates, fields=[
#             'upper_basket_num', 'upper_basket_changed_time',
#             'lower_basket_num', 'lower_basket_changed_time',
#             'upper_rail_state', 'lower_rail_state',
#             'state', 'is_connected'
#         ])
#         PlatFormRealInfo.objects.filter(id__in=basket_update_ids).update(last_updated_time=datetime.datetime.now())


def collect_basket_num():
    """定时获取站台花篮数"""
    plts = PlatFormRealInfo.objects.filter(
        platform_info__location_name__isnull=False).select_related('platform_info')
    wcs_url = Configuration.objects.get(key='wcs_url').value
    basket_updates = []
    plts.update(begin_time=datetime.datetime.now())
    plt_instance_dict = {i.platform_info.location_name: i for i in plts}
    if wcs_url:
        device_names = list(plts.values_list('platform_info__location_name', flat=True))
        ret = batch_request_wcs(wcs_url, device_names, 'GZ_AGVInfo')
        for lc_name, data in ret.items():
            plt_instance = plt_instance_dict.get(lc_name)
            if plt_instance:
                if data['msg'] == 'success':
                    dv = data['data'][0]['content'].split(',')
                    collect_logger.info('站台：{}, WCS点位信息：{}，'.format(lc_name, dv))
                    for idx, v in enumerate(dv):
                        try:
                            v = int(v)
                        except Exception:
                            continue
                        if idx == 0:
                            if plt_instance.upper_basket_num != v:
                                plt_instance.upper_basket_num = v
                                plt_instance.upper_basket_changed_time = datetime.datetime.now()
                        elif idx == 1:
                            if plt_instance.lower_basket_num != v:
                                plt_instance.lower_basket_num = v
                                plt_instance.lower_basket_changed_time = datetime.datetime.now()
                        elif idx == 2:
                            plt_instance.state = v
                        elif idx == 3:
                            plt_instance.upper_rail_state = v
                        elif idx == 4:
                            plt_instance.lower_rail_state = v
                    plt_instance.is_connected = True
                    plt_instance.last_updated_time = datetime.datetime.now()
                else:
                    collect_logger.error('站台：{}, 获取WCS信息失败！message：{}，'.format(lc_name, data['msg']))
                    plt_instance.is_connected = False
                basket_updates.append(plt_instance)

    # 批量更新
    if basket_updates:
        PlatFormRealInfo.objects.bulk_update(basket_updates, fields=[
            'upper_basket_num', 'upper_basket_changed_time',
            'lower_basket_num', 'lower_basket_changed_time',
            'upper_rail_state', 'lower_rail_state',
            'state', 'is_connected', 'last_updated_time'
        ])


if __name__ == '__main__':
    collect_basket_num()
    collect_stock_info()