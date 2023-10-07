import datetime

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView

from agv.models import Tasks
from basics.models import PlatFormInfo, Location, LocationGroupRelation
from mcs.derorators import api_recorder
from monitor.utils import get_agv_info


@method_decorator([api_recorder], name="dispatch")
class LocationSearchView(APIView):
    """RCS调用 查询休息位对应站台的优先级"""
    # [
    #         #     {
    #         #         'location_name': 'zrkd01',
    #         #         'fit_group': [
    #         #             {'machine_no': '1011', 'priority': 1}
    #         #         ],
    #         #         'if_relay': False,
    #         #         'if_active': True
    #         #     }
    #         # ]
    authentication_classes = ()

    def get(self, reqeust):
        data = []
        locations = Location.objects.all()
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
        return Response({"code": 0, "msg": 'success', 'data': data})


@method_decorator([api_recorder], name="dispatch")
class RCSAgvSearchView(APIView):
    """monitor调用 获取AGV列表及携带的物料信息"""
    # [
    #     {
    #         "agv_id": 1,  # 车号
    #         "status": 3,  # 1-离线，2-空闲，3-任务，4-充电，5-故障
    #         "task_dev_group": 'L8',  # AGV的目的地设备组名称，空花蓝传空""
    #         "rollers": [
    #             {"layer_no": 2,  # 层号 1-下层，2-上层
    #              "dev_group_no": "L7"
    #              },
    #             {"layer_no": 1,  # 层号 1-下层，2-上层
    #              "dev_group_no": "L7"
    #              }
    #         ]
    #     }
    # ]
    authentication_classes = ()

    def get_agv_info(self):
        data, code = get_agv_info()
        if code == 200 and "code" in data and data["code"] == 0:
            success_list = data["data"]['data']
            return success_list
        return []

    def get(self, request):
        agv_info = self.get_agv_info()
        if not agv_info:
            return Response({"code": 0, "msg": 'success', 'data': []})
        data = []
        current_tasks = dict(Tasks.objects.filter(state__in=(1, 2, 3, 4, 5, 6)).values_list('agv_no', 'end_location'))
        platform_group_dict = dict(PlatFormInfo.objects.filter(
            location_name__isnull=False, group__isnull=False).values_list('location_name', 'group__group_ID'))
        platform_location_dict = dict(PlatFormInfo.objects.filter(
            location_name__isnull=False).values_list('platform_ID', 'location_name'))
        for item in agv_info:
            task_dev_group = ''
            agv_id = item['agv_id']
            task_location = current_tasks.get(agv_id)
            if task_location:
                task_dev_group = platform_group_dict.get(task_location)
            data.append(
                {
                    'agv_id': agv_id,
                    'status': 2,
                    'task_dev_group': task_dev_group,
                    'task_loc': task_location,
                    'rollers': [
                        {"layer_no": 2, "dev_group_no": item['G2A']['machine_group'], 'src_loc': platform_location_dict.get(item['G2A']['machine_no'])},
                        {"layer_no": 1, "dev_group_no": item['G1A']['machine_group'], 'src_loc': platform_location_dict.get(item['G1A']['machine_no'])}
                    ]
                }
            )
        return Response({"code": 0, "msg": 'success', 'data': data})


@method_decorator([api_recorder], name="dispatch")
class PlatformGroupSearchView(APIView):
    """monitor调用：获取工作区下的所有设备组以及站台信息"""
    # [
    #     {
    #         "work_area": "gongzuoqu01",  # 工作区名称
    #         "device_groups": [
    #             {"group_name": 'L7',  # 设备组名称
    #              "stations": ['father_location71', 'father_location72']
    #              },
    #             {"group_name": 'L8',
    #              "stations": ['father_location81', 'father_location82']
    #              },
    #         ]
    #     }
    # ]
    authentication_classes = ()

    def get(self, request):
        platform_data = PlatFormInfo.objects.filter(
            location_name__isnull=False, group__isnull=False
        ).values('platform_ID', 'location_name', 'process__working_area__area_name', 'group__group_ID')

        work_areas = {}

        for item in platform_data:
            work_area = item['process__working_area__area_name']
            group_name = item['group__group_ID']
            station = item['location_name']

            if work_area not in work_areas:
                work_areas[work_area] = {'work_area': work_area, 'device_groups': []}

            device_groups = work_areas[work_area]['device_groups']

            group_info = next((g for g in device_groups if g['group_name'] == group_name), None)
            if group_info is None:
                group_info = {'group_name': group_name, 'stations': []}
                device_groups.append(group_info)

            group_info['stations'].append(station)

        result = list(work_areas.values())

        return Response({"code": 0, "msg": 'success', 'data': result})


@method_decorator([api_recorder], name="dispatch")
class PlatformSearchView(APIView):
    """monitor调用：获取所有站台信息"""
    # [
    #     {
    #         "work_area": "gongzuoqu01",  # 工作区名称
    #         "group_name": 'L7',  # 设备组名称
    #         "name": 'father_location71',  # 机台名
    #         "desc": 'F71',  # 机台简称
    #         "id": 71,  # 机台ID
    #         "status": 1,  # 机台状态 1：正常生产 2：缺料 3：故障 4：已屏蔽 5：其他
    #         "alarm_flag": 1,  # 断料报警 空：无预警 1：可能断料 2：一定断料
    #         "agv_id": 1,  # 车号
    #         "eta": 600,  # 单位s
    #         "rollers": [
    #             {
    #                 "layer_no": 2,  # 层号 1-下层，2-上层
    #                 "session_type": 1,  # 上下料类型 1-上料，2-下料
    #                 "hard_forbidden_enabled": False,  # 硬屏蔽
    #                 "thres": 8,  # 阈值 int
    #                 "blasket_num": 4,  # 花篮数 int
    #             },
    #             {
    #                 "layer_no": 1,  # 层号 1-下层，2-上层
    #                 "session_type": 2,  # 上下料类型 1-上料，2-下料
    #                 "hard_forbidden_enabled": False,  # 硬屏蔽
    #                 "thres": 2,  # 阈值 int
    #                 "blasket_num": 6,  # 花篮数 int
    #             }
    #         ]
    #     },
    # ]
    authentication_classes = ()

    def get(self, request):
        result = []
        platform_data = PlatFormInfo.objects.filter(
            location_name__isnull=False
        ).values('desc', 'platform_ID', 'location_name', 'process__working_area__area_name',
                 'group__group_ID', 'platform_real_info__state', 'platform_real_info__upper_rail_state',
                 'platform_real_info__lower_rail_state', 'platform_real_info__upper_basket_num',
                 'platform_real_info__lower_basket_num', 'is_used', 'process__upper_rail_type',
                 'process__lower_rail_type', 'up_task_trigger_threshold', 'down_task_trigger_threshold')
        state_dict = {4: 1, 5: 2, 6: 3}
        # current_task_dict = dict(Tasks.objects.filter(state__in=(2, 3, 4, 5, 6)).values_list('end_location', 'agv_no'))
        current_tasks = Tasks.objects.filter(state__in=(1, 2, 3, 4, 5, 6)).values('end_location', 'agv_no', 'state')
        current_task_dict = {i['end_location']: {'agv_no': i['agv_no'], 'state': i['state']} for i in current_tasks}
        agv_eta_time_dict = {}
        data, code = get_agv_info()
        if code == 200 and "code" in data and data["code"] == 0:
            success_list = data["data"]['data']
            for item in success_list:
                agv_eta_time_dict[item['agv_id']] = item['parameter_1']['eta_time']

        for item in platform_data:
            work_area = item['process__working_area__area_name']
            group_name = item['group__group_ID']
            name = item['location_name']
            desc = item['desc']
            platform_id = item['platform_ID']
            state = item['platform_real_info__state']
            is_used = item['is_used']
            upper_rail_type = item['process__upper_rail_type']
            lower_rail_type = item['process__lower_rail_type']
            up_task_trigger_threshold = item['up_task_trigger_threshold']
            down_task_trigger_threshold = item['down_task_trigger_threshold']
            up_basket_num = item['platform_real_info__upper_basket_num']  # 上料花篮数
            down_basket_num = item['platform_real_info__lower_basket_num']  # 下料花篮数
            up_rail_state = item['platform_real_info__upper_rail_state']  # 上料屏蔽
            down_rail_state = item['platform_real_info__lower_rail_state']  # 下料屏蔽
            eta = None
            if not is_used:
                platform_status = 4
            else:
                platform_status = state_dict.get(state, 5)
            upper_rail_state = lower_rail_state = upper_basket_num = lower_basket_num = upper_threshold = lower_threshold = None
            if upper_rail_type == 1:
                upper_basket_num = up_basket_num
                upper_rail_state = up_rail_state
                upper_threshold = up_task_trigger_threshold
            elif upper_rail_type == 2:
                upper_basket_num = down_basket_num
                upper_rail_state = down_rail_state
                upper_threshold = down_task_trigger_threshold
            if lower_rail_type == 1:
                lower_basket_num = up_basket_num
                lower_rail_state = up_rail_state
                lower_threshold = up_task_trigger_threshold
            elif lower_rail_type == 2:
                lower_basket_num = down_basket_num
                lower_rail_state = down_rail_state
                lower_threshold = down_task_trigger_threshold
            task_info = current_task_dict.get(name)
            agv_no = task_status = None
            if task_info:
                agv_no = task_info.get('agv_no')
                task_state = task_info.get('state')
                if task_state in (1, 2):
                    task_status = 1
                elif task_state == 3:
                    task_status = 2
                elif task_state == 4:
                    task_status = 3
                else:
                    task_status = 4
                if agv_no:
                    eta = int(agv_eta_time_dict.get(agv_no, 0))
            data = {
                "work_area": work_area,
                "group_name": group_name,
                "name": name,
                "desc": desc,
                "id": platform_id,
                "status": platform_status,
                "alarm_flag": None,
                "agv_id": agv_no,  # 车号
                "eta": eta,
                "task_state": task_status,
                "rollers": [
                    {
                        'layer_no': 1,  # 层
                        "session_type": lower_rail_type,  # 上下料类型 1-上料，2-下料
                        "hard_forbidden_enabled": True if lower_rail_state == 1 else False,  # 硬屏蔽
                        "thres": lower_threshold,  # 阈值 int
                        "blasket_num": lower_basket_num,  # 花篮数 int
                    },
                    {
                        'layer_no': 2,  # 层
                        "session_type": upper_rail_type,  # 上下料类型 1-上料，2-下料
                        "hard_forbidden_enabled": True if upper_rail_state == 1 else False,  # 硬屏蔽
                        "thres": upper_threshold,  # 阈值 int
                        "blasket_num": upper_basket_num,  # 花篮数 int
                    }
                ]
            }
            result.append(data)
        return Response({"code": 0, "msg": 'success', 'data': result})


@method_decorator([api_recorder], name="dispatch")
class PlatformLastTimeSearchView(APIView):
    """RCS调用：获取站台轨道预计最快对接完成时间"""

    def get(self, request):
        result = {}
        data = PlatFormInfo.objects.filter(location_name__isnull=False).values(
            'location_name', 'pitch_time', 'process__upper_rail_type', 'process__lower_rail_type',
            'platform_real_info__upper_basket_num', 'platform_real_info__lower_basket_num',
            'platform_real_info__upper_basket_changed_time', 'platform_real_info__lower_basket_changed_time',
            'process__single_slot_num'
            ).order_by('location_name')
        for item in data:
            up_rail_pred_time = lower_rail_pred_time = None
            pitch_time = item['pitch_time']
            location_name = item['location_name']
            slot_num = item['process__single_slot_num'] * 2  # 单层花篮数量
            upper_rail_type = item['process__upper_rail_type']
            lower_rail_type = item['process__lower_rail_type']
            up_basket_num = item['platform_real_info__upper_basket_num']
            down_basket_num = item['platform_real_info__lower_basket_num']
            upper_basket_changed_time = item['platform_real_info__upper_basket_changed_time']
            lower_basket_changed_time = item['platform_real_info__lower_basket_changed_time']
            if not upper_basket_changed_time:
                upper_basket_changed_time = datetime.datetime.now()
            if not lower_basket_changed_time:
                lower_basket_changed_time = datetime.datetime.now()
            if not up_basket_num:
                up_basket_num = 0
            if not down_basket_num:
                down_basket_num = 0
            if upper_rail_type == 1:  # 上层上料
                up_rail_pred_time = datetime.datetime.strftime(
                    upper_basket_changed_time + datetime.timedelta(seconds=up_basket_num * (pitch_time/slot_num)), '%Y-%m-%d %H:%M:%S')
            elif upper_rail_type == 2:  # 上层下料
                up_rail_pred_time = datetime.datetime.strftime(
                    upper_basket_changed_time + datetime.timedelta(seconds=(slot_num - down_basket_num) * (pitch_time/slot_num)), '%Y-%m-%d %H:%M:%S')
            if lower_rail_type == 1:  # 下层上料
                lower_rail_pred_time = datetime.datetime.strftime(
                    lower_basket_changed_time + datetime.timedelta(seconds=up_basket_num * (pitch_time/slot_num)), '%Y-%m-%d %H:%M:%S')
            elif lower_rail_type == 2:  # 下层下料
                lower_rail_pred_time = datetime.datetime.strftime(
                    lower_basket_changed_time + datetime.timedelta(seconds=(slot_num-down_basket_num) * (pitch_time/slot_num)), '%Y-%m-%d %H:%M:%S')
            result[location_name] = {'up_rail_pred_time': up_rail_pred_time, 'lower_rail_pred_time': lower_rail_pred_time}
        return Response({"code": 0, "msg": 'success', 'data': result})


@method_decorator([api_recorder], name="dispatch")
class PlatformLocationSearch(APIView):
    """RCS调用：根据机台名查询机台编号和设备组编号"""

    def get(self, request):
        result = []
        plt_data = PlatFormInfo.objects.filter(
            location_name__isnull=False
        ).values('location_name', 'platform_ID', 'platform_name', 'group__group_name', 'group__group_ID')
        for item in plt_data:
            result.append(
                {
                    'location_name': item['location_name'],
                    'platform_ID': item['platform_ID'],
                    'platform_name': item['platform_name'],
                    'group_ID': item['group__group_ID'],
                    'group_name': item['group__group_name'],
                }
            )
        return Response({"code": 0, "msg": 'success', 'data': result})