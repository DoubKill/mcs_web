import json

import requests

from basics.models import Configuration


def cancel_task(data):
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    rcs_url = Configuration.objects.get(key='rcs_url').value
    try:
        url = rcs_url + '/api/om/order/order-command/'
        response = requests.request("PUT", url, json=data, headers=headers, timeout=3)
    except Exception as e:
        return {"error": str(e)}, 400
    return response.text.encode('latin-1').decode('gbk'), response.status_code


def cancel_cache_device_task(location_name, cancel_type, group_no):
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    send_data = {
        "Request": {
            "deviceType": "mcs",
            "deviceName": location_name,
            "interfaceName": "UnloadTask_MCSRequestStack" if cancel_type == 'in' else "LoadTask_MCSRequestStack",
            "subInterfaceId": "",
            "control1": {
                "machine_group": group_no,
                "order_id": '0',
                "layer": '0',
                "request_stack": "3" if cancel_type == 'in' else "4"
            }
        }
    }
    wcs_url = Configuration.objects.get(key='wcs_url').value
    try:
        url = wcs_url + '/api/wcs/call_interface/?deviceName={}'.format(location_name)
        response = requests.request("POST", url, json=send_data, headers=headers, timeout=3)
        response.raise_for_status()
    except Exception as e:
        return str(e), 400
    resp_json_data = response.json()
    resp_data = resp_json_data['Response']
    if resp_data['Result'] == 'True':
        return '', 200
    else:
        return resp_data, 400


def get_agv_list():
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    rcs_url = Configuration.objects.get(key='rcs_url').value
    try:
        url = rcs_url + '/api/engine/basic-data/agvs/'
        response = requests.request("GET", url, headers=headers, timeout=5)
    except Exception as e:
        return {"error": str(e)}, 400
    try:
        rdata = json.loads(response.text.encode('latin-1').decode('gbk'))
    except Exception as e:
        return {"error": str(e)}, 400
    return rdata, response.status_code


def get_agv_info():
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    rcs_url = Configuration.objects.get(key='rcs_url').value
    try:
        url = rcs_url + '/api/dispatch/agv-slots/'
        response = requests.request("GET", url, headers=headers, timeout=3)
    except Exception as e:
        return {"error": str(e)}, 400
    try:
        rdata = json.loads(response.text.encode('latin-1').decode('gbk'))
    except Exception as e:
        return {"error": str(e)}, 400
    return rdata, response.status_code


def get_rest_locations():
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'charset': 'utf-8',
    }
    rcs_url = Configuration.objects.get(key='rcs_url').value
    try:
        url = rcs_url + '​/api​/dispatch​/universal​/basic-data​/locations​/rest_location​/'
        response = requests.request("GET", url, headers=headers, timeout=3)
    except Exception as e:
        return {"error": str(e)}, 400
    try:
        rdata = json.loads(response.text.encode('latin-1').decode('gbk'))
    except Exception as e:
        return {"error": str(e)}, 400
    return rdata, response.status_code
