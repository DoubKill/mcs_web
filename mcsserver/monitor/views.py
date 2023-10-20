import datetime
import json
import math
from copy import deepcopy

from django.db.models import Count, Sum, Q, F, Avg, DurationField

from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from agv.models import Tasks, CacheDeviceStock
from basics.models import PlatFormInfo, CacheDeviceInfo, ProcessSection, PlatformGroup, RoutingSchema, \
    CacheDeviceRouteRelation, RestLocationRouteRelation, PlatFormRealInfo
from basics.serializers import PlatformGroupSerializer
from mcs.common_code import CommonExportListMixin
from mcs.derorators import api_recorder
from monitor.filters import TaskMonitorFilter, AlarmFilter
from monitor.models import StockHistorySummary, AlarmLog
from monitor.serializers import TaskMonitorSerializer, AlarmSerializer, TaskHistorySerializer
from monitor.utils import cancel_task, get_agv_info


@method_decorator([api_recorder], name="dispatch")
class TaskMonitorViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = TaskMonitorSerializer
    queryset = Tasks.objects.filter(state__in=[1, 2, 3, 4, 5, 6])
    filter_class = TaskMonitorFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('created_time',)
    ordering = ['id']
    # def get_serializer_context(self):
    #     platform_location_dict = dict(PlatFormInfo.objects.values_list('location_name', 'platform_name'))
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self,
    #         'platform_location_dict': platform_location_dict
    #     }

    # def list(self, request, *args, **kwargs):
    #     cycle_location_name = self.request.query_params.get('cycle_location_name')  # 料架所处循环
    #     filter_state = self.request.query_params.get('filter_state')  # 任务状态
    #     queryset = self.filter_queryset(self.get_queryset())
    #     if cycle_location_name:
    #         rack_names = list(RackInfo.objects.filter(
    #             is_used=True, cycle_location__global_name=cycle_location_name
    #         ).values_list('rack_name', flat=True))
    #         queryset = queryset.filter(rack_name__in=rack_names)
    #     state_cnt_dict = dict(queryset.values('state').annotate(cnt=Count('id')).values_list('state', 'cnt'))
    #     task_cnt = queryset.count()
    #     # 状态过滤之前分组合计其他筛选条件下的状态数量
    #     if filter_state:
    #         queryset = queryset.filter(state=int(filter_state))
    #     data = self.get_serializer(queryset, many=True, ).data
    #     trace_backs = RCSOrderTraceback.objects.filter(task_no__in=queryset.values_list('task_no', flat=True))
    #     trace_back_data = RCSOrderTracebackSerializer(trace_backs, many=True).data
    #     trace_back_data_dict = {i['task_no']: i for i in trace_back_data}
    #     for item in data:
    #         item.update(trace_back_data_dict.get(item['task_no'], {}))
    #     return Response({'data': data, 'total_cnt': task_cnt, 'state_cnt_dict': state_cnt_dict})

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        opera_type = self.request.data.get('task_state')
        if opera_type == 1:  # 取消
            if not order.rcs_order_id:
                raise ValidationError('该任务暂未下发，无法取消！')
            data = [{'order_id': order.rcs_order_id, 'order_command_type_id': 2}]
            res_data, recode = cancel_task(data)
            if recode == 200:
                return Response('取消成功')
            else:
                return Response('任务取消失败：{}'.format(json.loads(res_data['msg'])))
        # elif opera_type == 2:  # 强制完成
        #     order.state = 7
        #     order.save()
        # else:
        #     raise ValidationError('未知操作类型')
        return Response('操作成功')


# @method_decorator([api_recorder], name="dispatch")
# class InventoryInProcessMonitorView(APIView):
#
#     def get(self, request):
#         processes = list(ProductionProcess.objects.order_by('ordering').values_list('process_name', flat=True))
#         ps_idx_dict = {ps: idx for idx, ps in enumerate(processes)}
#         ret = {
#             'processes': processes,
#             'agv': [0] * len(processes),
#             'stations': [0] * len(processes),
#         }
#         platform_process_dict = dict(PlatForm.objects.values_list(
#             'platform_code', 'equip__process__process_name'))
#
#         cache_device_stock_data = CacheDeviceStock.objects.values('platform_code').annotate(cnt=Count('id'))
#         rack_stock_info = RackInfo.objects.filter(platform__isnull=False).values(
#             'platform__equip__process__process_name').annotate(a1=Sum('axis1_basket_num'),
#                                                                a2=Sum('axis2_basket_num'),
#                                                                a3=Sum('axis3_basket_num'),
#                                                                a4=Sum('axis4_basket_num'))
#         for i in cache_device_stock_data:
#             process_name = platform_process_dict.get(i['platform_code'])
#             cnt = i['cnt']
#             if process_name not in ps_idx_dict:
#                 continue
#             process_idx = ps_idx_dict[process_name]
#             ret['stations'][process_idx] += cnt
#
#         for j in rack_stock_info:
#             process_name = j['platform__equip__process__process_name']
#             cnt = j['a1'] + j['a2'] + j['a3'] + j['a4']
#             if process_name not in ps_idx_dict:
#                 continue
#             process_idx = ps_idx_dict[process_name]
#             ret['agv'][process_idx] += cnt
#         return Response({'data': ret})
#
#
# @method_decorator([api_recorder], name="dispatch")
# class ErrorWarningMonitorView(APIView):
#
#     def get(self, request):
#         warning_type = self.request.query_params.get('warning_type')
#         qs = ErrorWarningMonitor.objects.all()
#         if warning_type:
#             qs = qs.filter(warning_type=warning_type)
#         return Response({"data": qs.values('message', 'warning_type'),
#                          'warning_types': dict(ErrorWarningMonitor.WARNING_TYPE_CHOICE)})
#
#
# @method_decorator([api_recorder], name="dispatch")
# class BasketTransportMonitorView(CommonExportListMixin, ListAPIView):
#     queryset = BasketTransportMonitor.objects.order_by('-id')
#     serializer_class = BasketTransportMonitorSerializer
#     filter_class = BasketTransportMonitorFilter
#     EXPORT_FIELDS_DICT = {
#         '花篮RFID': 'rfid',
#         '工序': 'process_name',
#         '设备': 'equip_name',
#         '站台': 'platform_name',
#         '轴号': 'axis',
#         'AGV/货架编号': 'vehicle_code',
#         '传篮开始时间': 'begin_time',
#         '传篮完成时间': 'end_time'
#     }
#     FILE_NAME = '花篮RFID追溯.xlsx'
#
#
# @method_decorator([api_recorder], name="dispatch")
# class CacheLocationMonitorView(APIView):
#
#     def get(self, request):
#         ret = []
#         # district_id = self.request.query_params.get('district')
#         location_code = self.request.query_params.get('location_code')
#         filter_state = self.request.query_params.get('filter_state')
#         agv_id = self.request.query_params.get('agv_id')
#         locations = Location.objects.filter(is_used=True).order_by('location_type', 'location_code')
#         state_cnt_dict = {}
#         # if district_id:
#         #     locations = locations.filter(district_id=district_id)
#         if location_code:
#             locations = locations.filter(location_code__icontains=location_code)
#         if agv_id:
#             locations = locations.filter(Q(rack_info=agv_id) | Q(locked_rack_info=agv_id))
#         location_data = locations.values('id', 'location_code', 'rack_info__rack_name',
#                                          'rack_info__recipe_time', 'locked_rack_info__rack_name')
#         for location in location_data:
#             location_code = location['location_code']
#             state = '空闲'  # ['空闲', '已占用', '锁定', '锁定超时']
#             last_time = ''
#             rack_name = ''
#             locked_rack_name = ''
#             if location['rack_info__rack_name']:
#                 state = '已占用'
#                 if location['rack_info__recipe_time']:
#                     last_time = int((datetime.datetime.now() - location['rack_info__recipe_time']).total_seconds())
#                     # if last_time > location.rack_info.real_info.platform.equip.process.q_time * 60:
#                     #     state = '锁定超时'
#                 rack_name = location['rack_info__rack_name']
#             if location['locked_rack_info__rack_name']:
#                 state = '锁定'
#                 locked_rack_name = location['locked_rack_info__rack_name']
#             ret.append({'location_code': location_code,
#                         'state': state,
#                         'left_time': last_time,
#                         'id': location['id'],
#                         'rack_name': rack_name,
#                         'locked_rack_name': locked_rack_name})
#             state_cnt_dict[state] = state_cnt_dict.get(state, 0) + 1
#         if filter_state:
#             ret = list(filter(lambda x: x['state'] == filter_state, ret))
#         return Response({'data': ret, 'total_cnt': locations.count(), 'state_cnt_dict': state_cnt_dict})
#
#
# @method_decorator([api_recorder], name="dispatch")
# class CacheLocationDetailMonitorView(APIView):
#
#     def get(self, request):
#         location_id = self.request.query_params.get('location_id')
#         location = Location.objects.get(id=location_id)
#         if location.rack_info:  # 当前位置有料架
#             agv_no = location.rack_info.rack_name  # 一体车料架名称就是AGV名称
#             axis_num = location.rack_info.rack_type.axis_num  # 轴数
#             basket_nums = location.rack_info.rack_type.basket_num  # 每轴可放花篮数量
#             if location.rack_info.platform:
#                 process = location.rack_info.platform.equip.process.process_name  # 工序
#                 material_type = location.rack_info.platform.out_port_material_type.port_material_type_name  # 物料类型
#             else:
#                 process = ''
#                 material_type = ''
#             rack = location.rack_info
#         elif location.locked_rack_info:  # 当前料架被锁定
#             agv_no = location.locked_rack_info.rack_name  # 一体车料架名称就是AGV名称
#             axis_num = location.locked_rack_info.rack_type.axis_num  # 轴数
#             basket_nums = location.locked_rack_info.rack_type.basket_num  # 每轴可放花篮数量
#             if location.locked_rack_info.platform:
#                 process = location.locked_rack_info.platform.equip.process.process_name  # 工序
#                 material_type = location.locked_rack_info.platform.out_port_material_type.port_material_type_name  # 物料类型
#             else:
#                 process = ''
#                 material_type = ''
#             rack = location.locked_rack_info
#         else:
#             return Response({})
#
#         # 料架货位当前花篮数量
#         rack_location_data = {1: {'axis': 1,
#                                   'num': rack.axis1_basket_num,
#                                   'process': '' if not rack.axis1_basket_num else process,
#                                   'material_type': '' if not rack.axis1_basket_num else material_type
#                                   },
#                               2: {'axis': 2,
#                                   'num': rack.axis2_basket_num,
#                                   'process': '' if not rack.axis2_basket_num else process,
#                                   'material_type': '' if not rack.axis2_basket_num else material_type
#                                   },
#                               3: {'axis': 3,
#                                   'num': rack.axis3_basket_num,
#                                   'process': '' if not rack.axis3_basket_num else process,
#                                   'material_type': '' if not rack.axis3_basket_num else material_type
#                                   },
#                               4: {'axis': 4,
#                                   'num': rack.axis4_basket_num,
#                                   'process': '' if not rack.axis4_basket_num else process,
#                                   'material_type': '' if not rack.axis4_basket_num else material_type
#                                   }}
#         task_no = ''  # 任务号
#         state = '空闲'  # AGV状态
#         agv_last_task = Tasks.objects.filter(rack_name=agv_no).order_by('id').last()  # AGV最后一条任务
#         if agv_last_task:
#             if agv_last_task.state in [1, 2]:
#                 state = '任务'
#                 task_no = agv_last_task.task_no
#                 # action = agv_last_task.get_action_display()
#                 if agv_last_task.axis1_action:
#                     rack_location_data[1]['task_no'] = task_no
#                     rack_location_data[1]['action'] = agv_last_task.get_axis1_action_display()
#                 if agv_last_task.axis2_action:
#                     rack_location_data[2]['task_no'] = task_no
#                     rack_location_data[2]['action'] = agv_last_task.get_axis2_action_display()
#                 if agv_last_task.axis3_action:
#                     rack_location_data[3]['task_no'] = task_no
#                     rack_location_data[3]['action'] = agv_last_task.get_axis3_action_display()
#                 if agv_last_task.axis4_action:
#                     rack_location_data[4]['task_no'] = task_no
#                     rack_location_data[4]['action'] = agv_last_task.get_axis4_action_display()
#         data = {
#             'agv_no': agv_no,
#             'state': state,
#             'task_no': task_no,
#             'basket_data': rack_location_data.values(),
#             'basket_nums': basket_nums,
#             'axis_num': axis_num
#         }
#         return Response(data)


@method_decorator([api_recorder], name="dispatch")
class AGVMonitorView(APIView):

    def get_agv_info(self):
        data, code = get_agv_info()
        if code == 200 and "code" in data and data["code"] == 0:
            success_list = data["data"]['data']
            return success_list
        raise ValidationError('获取AGV列表失败')

    def get(self, request):
        ret = []
        state_cnt_dict = {}
        filter_state = self.request.query_params.get('filter_state')  # 小车状态过滤: 空闲、任务
        agv_info = self.get_agv_info()
        total_cnt = len(agv_info)
        for vehicle in agv_info:
            parameter_1 = vehicle.get('parameter_1')
            state = parameter_1['agv_status']
            battery_percent = parameter_1['agv_battery'] * 100
            ax1 = vehicle['G2A']['machine_no']
            ax3 = vehicle['G1A']['machine_no']
            ret.append({'vehicle_code': vehicle['agv_id'],
                        'state': state,
                        'battery_percent': '' if not battery_percent else int(battery_percent),
                        'vehicle_id': vehicle['agv_id'],
                        'upper_full': True if ax1 else False,
                        'lower_full': True if ax3 else False
                        })
            state_cnt_dict[state] = state_cnt_dict.get(state, 0) + 1
        if filter_state:
            ret = list(filter(lambda x: x['state'] == int(filter_state), ret))
        ret = sorted(ret, key=lambda x: x['vehicle_code'])
        return Response({'data': ret, 'total_cnt': total_cnt, 'state_cnt_dict': state_cnt_dict})


@method_decorator([api_recorder], name="dispatch")
class AGVDetailMonitorView(APIView):

    def get_agv_info(self):
        data, code = get_agv_info()
        if code == 200 and "code" in data and data["code"] == 0:
            success_list = data["data"]['data']
            return success_list
        raise ValidationError('获取AGV列表失败')

    def get(self, request):
        agv_no = self.request.query_params.get('vehicle_id')
        if not agv_no:
            raise ValidationError('请选择正确的AGV！')
        agv_no = int(agv_no)
        agv_info = self.get_agv_info()
        current_agv = list(filter(lambda x: x['agv_id'] == agv_no, agv_info))
        if not current_agv:
            return Response({})
        current_position = current_agv[0]['position']  # 当前位置
        ax1 = current_agv[0]['G2A']
        ax2 = current_agv[0]['G2B']
        ax3 = current_agv[0]['G1A']
        ax4 = current_agv[0]['G1B']
        parameter_1 = current_agv[0].get('parameter_1')
        state = parameter_1['agv_status']
        battery_percent = parameter_1['agv_battery'] * 100
        # ax1_basket_num = parameter_1['roller_num']['G2A']
        # ax2_basket_num = parameter_1['roller_num']['G2B']
        # ax3_basket_num = parameter_1['roller_num']['G1A']
        # ax4_basket_num = parameter_1['roller_num']['G1B']
        task_no = None
        out_time = None
        agv_task = Tasks.objects.filter(agv_no=agv_no, state__in=(1, 2, 3, 4, 5, 6)).last()
        finished_agv_task = Tasks.objects.filter(agv_no=agv_no, state=7).order_by('id').last()
        if agv_task:
            task_no = agv_task.task_no
        if finished_agv_task:
            out_time = finished_agv_task.end_time.strftime('%Y-%m-%d %H:%M:%S')
        platform_dict = dict(PlatFormInfo.objects.values_list('platform_ID', 'platform_name'))
        process_dict = dict(ProcessSection.objects.values_list('process_ID', 'process_name'))
        group_dict = dict(PlatformGroup.objects.values_list('group_ID', 'group_name'))
        basket_data = [
            {'axis': 1,  # G2A
             'out_time': ax1['roll_basket_ready_time'],
             'qtime': ax1['qtime'],
             'num': 5 if ax1['machine_no'] else None,
             'process': process_dict.get(ax1['craft_id']),
             'machine_no': platform_dict.get(ax1['machine_no']),
             'material_type': group_dict.get(ax1['machine_group'], ax1['machine_group']),
             },
            {'axis': 2,  # G2B
             'out_time': ax2['roll_basket_ready_time'],
             'qtime': ax2['qtime'],
             'num': 5 if ax2['machine_no'] else None,
             'process': process_dict.get(ax2['craft_id']),
             'machine_no': platform_dict.get(ax2['machine_no']),
             'material_type': group_dict.get(ax2['machine_group'], ax2['machine_group']),
             },
            {'axis': 3,  # G1A
             'out_time': ax3['roll_basket_ready_time'],
             'qtime': ax3['qtime'],
             'num': 5 if ax3['machine_no'] else None,
             'process': process_dict.get(ax3['craft_id']),
             'machine_no': platform_dict.get(ax3['machine_no']),
             'material_type': group_dict.get(ax3['machine_group'], ax3['machine_group']),
             },
            {'axis': 4,  # G1B
             'out_time': ax4['roll_basket_ready_time'],
             'qtime': ax4['qtime'],
             'num': 5 if ax4['machine_no'] else None,
             'process': process_dict.get(ax4['craft_id']),
             'machine_no': platform_dict.get(ax4['machine_no']),
             'material_type': group_dict.get(ax4['machine_group'], ax4['machine_group']),
             }
        ]

        data = {
            'agv_no': agv_no,  # 小车号
            'basket_nums': 5,  # 每轴可放花篮数量
            'battery_percent': '' if not battery_percent else '{}%'.format(str(int(battery_percent))),  # 电量比
            'location_code': current_position,  # 当前位置
            'axis_num': 4,  # 轴数
            'state': state,  # AGV 状态
            'task_no': task_no,  # 任务号
            'basket_data': basket_data  # 轨道花篮及物料规格
        }
        return Response(data)


@method_decorator([api_recorder], name="dispatch")
class AGVPackageMonitorView(APIView):

    def get_agv_info(self):
        data, code = get_agv_info()
        if code == 200 and "code" in data and data["code"] == 0:
            success_list = data["data"]['data']
            return success_list
        raise ValidationError('获取AGV列表失败')

    def get(self, request):
        ret = []
        agv_info = self.get_agv_info()
        group_dict = dict(PlatformGroup.objects.values_list('group_ID', 'group_name'))
        plt_dict = dict(PlatFormInfo.objects.values_list('platform_ID', 'platform_name'))
        che_dict = dict(CacheDeviceInfo.objects.values_list('device_ID', 'device_name'))
        plt_dict.update(che_dict)

        vehicle_code_f = self.request.query_params.get('vehicle_code')
        ax1_material_f = self.request.query_params.get('ax1_material')
        ax2_material_f = self.request.query_params.get('ax2_material')
        ax3_material_f = self.request.query_params.get('ax3_material')
        ax4_material_f = self.request.query_params.get('ax4_material')
        is_expired_f = self.request.query_params.get('is_expired')
        out_time_f = self.request.query_params.get('out_time')
        platform_name_f = self.request.query_params.get('platform_name')
        now_time = datetime.datetime.now()
        for vehicle in agv_info:
            ax1_group_ID = vehicle['G2A']['machine_group']
            ax2_group_ID = vehicle['G2B']['machine_group']
            ax3_group_ID = vehicle['G1A']['machine_group']
            ax4_group_ID = vehicle['G1B']['machine_group']
            ax1_machine_ID = vehicle['G2A']['machine_no']
            ax3_machine_ID = vehicle['G1A']['machine_no']
            rail1_roll_basket_ready_time = vehicle['G1A']['roll_basket_ready_time']
            rail2_roll_basket_ready_time = vehicle['G2A']['roll_basket_ready_time']

            ax1_material = group_dict.get(ax1_group_ID, ax1_group_ID)
            ax2_material = group_dict.get(ax2_group_ID, ax2_group_ID)
            ax3_material = group_dict.get(ax3_group_ID, ax3_group_ID)
            ax4_material = group_dict.get(ax4_group_ID, ax4_group_ID)

            is_expired = 0
            platform_name = ''
            if rail1_roll_basket_ready_time and ax3_group_ID:
                platform_name = plt_dict.get(ax3_machine_ID, ax3_machine_ID)

                q_time = vehicle['G1A']['qtime']
                time_diff = (now_time - datetime.datetime.strptime(rail1_roll_basket_ready_time.split('.')[0],
                                                                   '%Y-%m-%d %H:%M:%S')).total_seconds()
                if time_diff > q_time:
                    is_expired = 1
            elif rail2_roll_basket_ready_time and ax1_group_ID:
                platform_name = plt_dict.get(ax1_machine_ID, ax1_machine_ID)
                q_time = vehicle['G2A']['qtime']
                time_diff = (now_time - datetime.datetime.strptime(rail2_roll_basket_ready_time.split('.')[0],
                                                                   '%Y-%m-%d %H:%M:%S')).total_seconds()
                if time_diff > q_time:
                    is_expired = 1

            ret.append({'vehicle_code': vehicle['agv_id'],
                        'ax1_material': ax1_material,
                        'ax2_material': ax2_material,
                        'ax3_material': ax3_material,
                        'ax4_material': ax4_material,
                        'platform_name': platform_name,
                        'out_time': rail1_roll_basket_ready_time or rail2_roll_basket_ready_time,
                        'is_expired': is_expired
                        })
        ret = sorted(ret, key=lambda x: x['vehicle_code'])
        if vehicle_code_f:
            ret = filter(lambda x: int(vehicle_code_f) == x['vehicle_code'], ret)
        if ax1_material_f:
            ret = filter(lambda x: ax1_material_f in x['ax1_material'], ret)
        if ax2_material_f:
            ret = filter(lambda x: ax2_material_f in x['ax2_material'], ret)
        if ax3_material_f:
            ret = filter(lambda x: ax3_material_f in x['ax3_material'], ret)
        if ax4_material_f:
            ret = filter(lambda x: ax4_material_f in x['ax4_material'], ret)
        if out_time_f:
            ret = filter(lambda x: out_time_f in x['out_time'], ret)
        if is_expired_f:
            ret = filter(lambda x: int(is_expired_f) == x['is_expired'], ret)
        if platform_name_f:
            ret = filter(lambda x: platform_name_f in x['platform_name'], ret)
        return Response({'data': list(ret)})


# @method_decorator([api_recorder], name="dispatch")
# class PlatformMonitorView(APIView):
#
#     def get(self, request):
#         ret = {i: {} for i in ProductionProcess.objects.values_list('process_name', flat=True)}
#         process_id = self.request.query_params.get('process_id')
#         filter_state = self.request.query_params.get('filter_state')
#         platforms = PlatForm.objects.filter(is_used=True, equip__equip_type=1).order_by(
#             'equip__process__ordering', 'equip__equip_name', 'platform_code')
#         if process_id:
#             platforms = platforms.filter(equip__process_id=process_id)
#         agv_task = list(Tasks.objects.filter(
#             state__in=[1, 2]).values_list('end_location', flat=True))
#         state_cnt_dict = dict()
#         platform_data = platforms.values('id', 'platform_code', 'location__location_code', 'equip__equip_name',
#                                          'equip__process__process_name', 'platform_name')
#         for platform in platform_data:
#             platform_code = platform['platform_code']
#             platform_location = platform['location__location_code']
#             state = '空闲' if platform_location not in agv_task else '任务'  # ['空闲', '任务']
#             state_cnt_dict[state] = state_cnt_dict.get(state, 0) + 1
#             if filter_state:
#                 if state != filter_state:
#                     continue
#             process_name = platform['equip__process__process_name']
#             equip_name = platform['equip__equip_name']
#             data = {'platform_code': platform_code,
#                     'platform_name': platform['platform_name'],
#                     'state': state,
#                     'id': platform['id'],
#                     'process': process_name,
#                     'equip_name': equip_name}
#             if equip_name in ret[process_name]:
#                 ret[process_name][equip_name].append(data)
#             else:
#                 ret[process_name][equip_name] = [data]
#         return Response({'data': ret, 'total_cnt': platforms.count(), 'state_cnt_dict': state_cnt_dict})
#
#
# @method_decorator([api_recorder], name="dispatch")
# class PlatformDetailMonitorView(APIView):
#
#     def get(self, request):
#         platform_id = self.request.query_params.get('platform_id')
#         platform = PlatForm.objects.get(id=platform_id)
#         if not hasattr(platform, 'platform_parts'):
#             return Response({})
#         agv_task = Tasks.objects.filter(end_location=platform.location.location_code).order_by('id').last()
#         platform_part_data = platform.platform_parts.order_by('axis').values('part_code', 'axis', 'part_type',
#                                                                              'threshold')
#         basket_nums = 5  # 每轴可放花篮数量
#         task_no = ''
#         agv_no = ''
#         axis_num = len(platform_part_data)  # 轴数
#         rack_location_data = []
#         for i in platform_part_data:
#             i['state'] = '开启对接'
#             i['task_type'] = '取货' if i['part_type'] == 1 else '卸货'
#             i['current_basket_num'] = 2
#             rack_location_data.append(i)
#         if agv_task:
#             if agv_task.state in [1, 2]:
#                 task_no = agv_task.task_no
#                 agv_no = agv_task.rack_name
#         data = {
#             'platform_code': platform.platform_code,
#             'agv_no': agv_no,
#             'task_no': task_no,
#             'basket_data': rack_location_data,
#             'axis_num': axis_num,
#             'basket_nums': basket_nums
#         }
#         return Response(data)


@method_decorator([api_recorder], name="dispatch")
class CacheStationMonitorView(APIView):

    def get(self, request):
        ret = []
        equips = CacheDeviceInfo.objects.all()
        total_locations = equips.aggregate(cnt=Sum(F('row_num') * F('column_num') * F('layer_num')))['cnt']
        equip_data = equips.values('id', 'device_name', 'in_is_used', 'out_is_used',
                                   'row_num', 'column_num', 'layer_num')
        # 堆栈花篮数量
        cache_device_stock_data1 = dict(CacheDeviceStock.objects.values(
            'equip_code').annotate(cnt=Sum('basket_num')).values_list('equip_code', 'cnt'))
        # 堆栈已使用库位
        cache_device_stock_data2 = dict(CacheDeviceStock.objects.filter(basket_num__gt=0).values(
            'equip_code').annotate(cnt=Count('id')
                                   ).values_list('equip_code', 'cnt'))
        # 含有超时物料的堆栈
        overtime_stock = dict(CacheDeviceStock.objects.filter().values('equip_code')
                              .annotate(over_num=Count('id', filter=Q(q_time__lt=F('output_time_consume') + F('storge_time'))))
                              .values_list('equip_code', 'over_num'))
        for equip in equip_data:
            equip_name = equip['device_name']
            row_num = equip['row_num']
            column_num = equip['column_num']
            layer_num = equip['layer_num']
            in_is_used = equip['in_is_used']
            out_is_used = equip['out_is_used']
            basket_num = cache_device_stock_data1.get(equip_name, 0)
            used_storage_location = cache_device_stock_data2.get(equip_name, 0)
            overtime_storage_location = overtime_stock.get(equip_name, 0)
            data = {'equip_name': equip_name,
                    'id': equip['id'],
                    'in_is_used': in_is_used,
                    'out_is_used': out_is_used,
                    'basket_num': basket_num,  # 花篮数
                    'total_storage_location': row_num*column_num*layer_num,
                    'used_storage_location': used_storage_location,
                    'overtime_storage_location': overtime_storage_location,
                    'specification': '{}_{}_{}'.format(row_num, column_num, layer_num),
                    'overtime_flag': False if overtime_storage_location == 0 else True
                    }
            ret.append(data)
        return Response({'data': ret, 'total_locations': 0 if not total_locations else total_locations,
                         'used_location': sum(cache_device_stock_data2.values()),
                         'total_basket_num': sum(cache_device_stock_data1.values())})


@method_decorator([api_recorder], name="dispatch")
class CacheStationDetailMonitorView(APIView):

    def get(self, request):
        equip_id = self.request.query_params.get('equip_id')
        equip = CacheDeviceInfo.objects.get(id=equip_id)
        ret = {}
        # layer_num = equip.layer_num
        # column_num = equip.column_num
        # row_num = equip.row_num
        storage_num = equip.storage_num
        equip_code = equip.device_name
        group_name_dict = dict(PlatformGroup.objects.values_list('group_ID', 'group_name'))
        cache_device_stock_data = (CacheDeviceStock.objects.filter(
            equip_code=equip_code).values(
            'row', 'column', 'layer', 'in_material_type_name', 'basket_num', 'output_time_consume', 'q_time', 'layoff_time', 'storge_time')
                                   .order_by('layer', 'row', 'column'))
        # 当前时间
        now_time = datetime.datetime.now()
        for item in cache_device_stock_data:
            layer = item['layer']
            row = item['row']
            column = item['column']
            group_ID = item['in_material_type_name']
            material_type = group_name_dict.get(group_ID, group_ID)
            basket_num = item['basket_num']
            output_time_consume = item['output_time_consume']
            storge_time = item['storge_time']
            q_time = item['q_time']
            overtime_flag = True if all([output_time_consume, q_time]) and q_time < (output_time_consume + storge_time) else False
            layoff_time = item['layoff_time']
            if layer not in ret:
                ret[layer] = {row: [{'layer': layer,
                                     'row': row,
                                     'column': column,
                                     'material_type': material_type,
                                     'basket_num': basket_num,
                                     'storage_num': storage_num,
                                     'equip_code': equip_code,
                                     'trans_time': layoff_time,
                                     'overtime_flag': overtime_flag,
                                     'q_time': q_time
                                     }]}
            else:
                if row in ret[layer]:
                    ret[layer][row].append({'layer': layer,
                                            'row': row,
                                            'column': column,
                                            'material_type': material_type,
                                            'basket_num': basket_num,
                                            'storage_num': storage_num,
                                            'equip_code': equip_code,
                                            'trans_time': layoff_time,
                                            'overtime_flag': overtime_flag,
                                            'q_time': q_time
                                            })
                else:
                    ret[layer][row] = [{'layer': layer,
                                        'row': row,
                                        'column': column,
                                        'material_type': material_type,
                                        'basket_num': basket_num,
                                        'storage_num': storage_num,
                                        'equip_code': equip_code,
                                        'trans_time': layoff_time,
                                        'overtime_flag': overtime_flag,
                                        'q_time': q_time
                                        }]
        # cache_device_stock_dict = {
        #     '{}-{}-{}'.format(i['row'], i['column'], i['layer']): {'cnt': i['basket_num'], 'mt': i['in_material_type_name']}
        #     for i in cache_device_stock_data}
        # for i in range(1, layer_num+1):
        #     for j in range(1, row_num+1):
        #         for k in range(1, column_num+1):
        #             l_stock_data = cache_device_stock_dict.get('{}-{}-{}'.format(j, k, i), {})
        #             basket_num = 0
        #             material_type = ''
        #             if l_stock_data:
        #                 basket_num = l_stock_data['cnt']
        #                 material_type = l_stock_data['mt']
        #             if i not in ret:
        #                 ret[i] = {j: [{'layer': i,
        #                                'row': j,
        #                                'column': k,
        #                                'material_type': material_type,
        #                                'basket_num': basket_num,
        #                                'storage_num': storage_num,
        #                                'equip_code': equip_code
        #                                }]}
        #             else:
        #                 if j in ret[i]:
        #                     ret[i][j].append({'layer': i,
        #                                        'row': j,
        #                                        'column': k,
        #                                        'material_type': material_type,
        #                                        'basket_num': basket_num,
        #                                        'storage_num': storage_num,
        #                                        'equip_code': equip_code
        #                                        })
        #                 else:
        #                     ret[i][j] = [{'layer': i,
        #                                    'row': j,
        #                                    'column': k,
        #                                    'material_type': material_type,
        #                                    'basket_num': basket_num,
        #                                    'storage_num': storage_num,
        #                                    'equip_code': equip_code
        #                                    }]
        return Response({'data': ret})


# @method_decorator([api_recorder], name="dispatch")
# class AGVTaskMonitorView(APIView):
#
#     def get(self, request, *args, **kwargs):
#         task_no = self.request.query_params.get('task_no')  # 任务号
#         task_type = self.request.query_params.get('task_type')  # 任务类型
#         platform_location_code = self.request.query_params.get('platform_code')  # 终点
#         vehicle_name = self.request.query_params.get('vehicle_code')  # AGV车号
#         filter_state = self.request.query_params.get('filter_state')  # 任务状态
#         queryset = RackInfo.objects.filter(rcs_agv_info__isnull=False)
#         vehicle_cnt = queryset.count()  # AGV总数
#         agv_tasks = Tasks.objects.filter(state__in=[1, 2])  # 进行中的任务
#         all_task_agv_nos = list(agv_tasks.values_list('rack_name', flat=True))  # 正在进行任务的AGV车号
#         all_task_data = agv_tasks.values('rack_name', 'task_no', 'end_location',
#                                          'axis1_action', 'axis2_action', 'axis3_action', 'axis4_action')
#         task_agv_cnt = len(set(all_task_agv_nos))  # 正在进行任务的AGV总数
#         state_cnt_dict = dict(queryset.values(
#             'rcs_agv_info__state'
#         ).annotate(cnt=Count('id')).values_list('rcs_agv_info__state', 'cnt'))
#         if task_no:
#             task_agv_nos = list(agv_tasks.filter(task_no__icontains=task_no).values_list('rack_name', flat=True))
#             queryset = queryset.filter(rack_name__in=task_agv_nos)
#         if task_type:
#             if task_type == '取货':
#                 task_type_agv_nos = list(agv_tasks.filter(Q(axis1_action=1) |
#                                                           Q(axis3_action=1)).values_list('rack_name', flat=True))
#             elif task_type == '卸货':
#                 task_type_agv_nos = list(agv_tasks.filter(Q(axis1_action=2) |
#                                                           Q(axis3_action=2)).values_list('rack_name', flat=True))
#             else:
#                 task_type_agv_nos = list(agv_tasks.filter(axis1_action__in=(1, 2),
#                                                           axis3_action__in=(1, 2)).values_list('rack_name', flat=True))
#             queryset = queryset.filter(rack_name__in=task_type_agv_nos)
#         if platform_location_code:
#             ep_agv_nos = list(agv_tasks.filter(end_location=platform_location_code).values_list('rack_name', flat=True))
#             queryset = queryset.filter(rack_name__in=ep_agv_nos)
#         if vehicle_name:
#             queryset = queryset.filter(rack_name=vehicle_name)
#         if filter_state:
#             queryset = queryset.filter(rcs_agv_info__state=filter_state)
#
#         platform_location_dict = dict(PlatForm.objects.values_list('location__location_code', 'platform_name'))
#
#         ret = []
#         rack_infos = list(RackInfo.objects.filter(
#             rcs_agv_info__isnull=False).values('rack_name', 'axis1_basket_num', 'axis2_basket_num',
#                                                   'axis3_basket_num', 'axis4_basket_num',
#                                                   'recipe_time', 'rack_type__basket_num',
#                                                   'material_type__port_material_type_name', 'rcs_agv_info__state'))
#
#         for vehicle_name in queryset.order_by('rcs_agv_info__rcs_agv_id').values_list('rack_name', flat=True):
#             item_racks = list(filter(lambda x: x['rack_name'] == vehicle_name, rack_infos))
#             if not item_racks:
#                 continue
#             item_rack = item_racks[0]
#             platform_name = ''  # 来源站台
#             stock_num = item_rack['rack_type__basket_num']  # AGV可放置花篮数
#             material_type_name = item_rack['material_type__port_material_type_name']  # 物料类型
#             basket_time = '' if not item_rack['recipe_time'] else item_rack['recipe_time'].strftime(
#                 "%Y-%m-%d %H:%M:%S")  # 花篮时间
#             state = item_rack['rcs_agv_info__state']
#             vehicle_tasks = list(filter(lambda x: x['rack_name'] == vehicle_name, all_task_data))
#             axis1_action = axis2_action = axis3_action = axis4_action = None
#             if vehicle_tasks:
#                 vehicle_task = vehicle_tasks[0]
#                 task_no = vehicle_task['task_no']
#                 task_end_location = vehicle_task['end_location']
#                 platform_name = platform_location_dict.get(task_end_location, '')
#                 axis1_action = vehicle_task['axis1_action']
#                 axis2_action = vehicle_task['axis2_action']
#                 axis3_action = vehicle_task['axis3_action']
#                 axis4_action = vehicle_task['axis4_action']
#             for idx, axis in enumerate([axis1_action, axis2_action, axis3_action, axis4_action]):
#                 if axis == 1:
#                     task_type = '取货'
#                 elif axis == 2:
#                     task_type = '卸货'
#                 else:
#                     task_type = ''
#                 item_data = {
#                     'vehicle_code': vehicle_name,
#                     'state': state,
#                     'level': '上层' if idx + 1 < 3 else '下层',
#                     'axis': idx + 1,
#                     'basket_num': item_rack['axis{}_basket_num'.format(str(idx + 1))],
#                     'stock_num': stock_num,
#                     'basket_time': '' if not axis else basket_time,
#                     'task_no': '' '' if not axis else task_no,
#                     'platform_name': '' if not axis else platform_name,
#                     'task_type_name': task_type,
#                     'material_type_name': '' if not axis else material_type_name
#                 }
#                 ret.append(item_data)
#         return Response({'data': ret, 'total_cnt': vehicle_cnt, 'state_cnt_dict': state_cnt_dict})
#

@method_decorator([api_recorder], name="dispatch")
class OrderHistoryView(CommonExportListMixin, ListAPIView):
    serializer_class = TaskHistorySerializer
    queryset = Tasks.objects.filter(state__in=[7, 8, 9])
    filter_class = TaskMonitorFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('created_time', 'arrived_time', 'end_time')
    ordering = ['-id']
    EXPORT_FIELDS_DICT = {
        '任务编号': 'task_no',
        '站台 ID': 'platform_ID',
        '站台名称': 'platform_name',
        '站台坐标': 'end_location',
        '小车编号': 'agv_no',
        '任务状态': 'state_name',
        '动作类型': 'task_type_name',
        '物料来源': 'origin_platform_name',
        '创建时间': 'created_time',
        '到位时间': 'arrived_time',
        '结束时间': 'end_time',
        '任务总耗时（秒）': 'task_time_consume',
        '小车行走耗时（秒）': 'task_move_consume',
        '任务交互耗时（秒）': 'task_interact_consume',
    }
    FILE_NAME = '历史任务.xlsx'


@method_decorator([api_recorder], name="dispatch")
class EquipStatusMonitorView(APIView):
    """table_head = [
        {'process_name': '制绒上', 'upper_rail_type': 1, 'lower_rail_type': None},
        {'process_name': '制绒下', 'upper_rail_type': 2, 'lower_rail_type': None},
        {'process_name': '鹏扩', 'upper_rail_type': 1, 'lower_rail_type': 2},
    ]
    table_data = {
    '制绒上': [
            {'dp_type': 1,  # 类型 1：站台 2：堆栈
             'instance_name': 'zrs01',  # 名称
             'upper_rail_num': 9,  # 上层花篮数
             'lower_rail_num': None,  # 下层花篮数
             'task_trigger_type': 1, # 上下料触发方式
             'upper_trigger_threshold': 4,  # 上层花篮阈值
             'lower_trigger_threshold': None,  # 下层花篮阈值
             'agv_no': None,  # AGV车号
             'task_state': None,  # 任务状态 1：已创建 2：已下发 3：已派车 4：已到达
             'plt_state': 0,  # 机台状态 0:失联 1：正常生产 2：缺料 3：故障 4：已屏蔽 5：其他
             'lower_rail_state': 1,  # 上层是否屏蔽 0:屏蔽 1:未屏蔽
             'upper_rail_state': None,  # 下层是否屏蔽 0:屏蔽 1:未屏蔽
             'alarm_flag': None  # 预警标记 NONE：无预警 1：可能断料 2：一定断料
             },
            {'dp_type': 2,  # 类型 1：站台 2：堆栈
             'instance_name': 'dz01',  # 名称
             'up_agv_no': None,  # 上料口AGV车号
             'down_agv_no': 1,  # 下料口AGV车号
             'up_task_state': 2,  # 上料口任务状态 1：已创建 2：已下发 3：已派车 4：已到达
             'down_task_state': 2,  # 下料口任务状态 1：已创建 2：已下发 3：已派车 4：已到达
             'plt_state': 1,  # 机台状态 1：正常生产 2：缺料 3：故障 4：已屏蔽 5：其他
             'total_locations': 27,  # 总库位数
             'used_locations': 5,  # 已占用库位数
             'process_used_locations': 2  # 当前工艺段已占用库位数
             },
             }],
    '制绒下': [],
    '鹏扩': []},
    }"""
    def get(self, request):
        dp_type = self.request.query_params.get('dp_type', '')
        processes = self.request.query_params.get('processes')
        working_area_id = self.request.query_params.get('working_area_id')
        ps_f_kwargs = {}
        pf_f_kwargs = {}
        dc_f_kwargs = {}
        if processes:
            processes_ids = [int(i) for i in processes.split(',')]
            ps_f_kwargs['id__in'] = processes_ids
            pf_f_kwargs['process_id__in'] = processes_ids
            dc_f_kwargs['group__process_id__in'] = processes_ids
        if working_area_id:
            ps_f_kwargs['working_area_id'] = working_area_id
            pf_f_kwargs['process__working_area_id'] = working_area_id
            dc_f_kwargs['cache_device__working_area_id'] = working_area_id

        # 表头
        table_head = list(ProcessSection.objects.filter(**ps_f_kwargs).order_by('ordering').values('process_name', 'upper_rail_type', 'lower_rail_type'))

        # 表体
        table_data = {p['process_name']: [] for p in table_head}
        #
        # if not dp_type:
        #     return Response({'table_head': table_head, 'table_data': table_data})

        dp_type_split = dp_type.split(',')

        # route_names = RoutingSchema.objects.order_by('id').values_list('route_name', flat=True)
        # for r in route_names:
        #     table_data[r] = {p['process_name']: [] for p in table_head}

        state_dict = {4: 1, 5: 2, 6: 3}
        current_tasks = Tasks.objects.filter(state__in=(1, 2, 3, 4, 5, 6)).values('end_location', 'agv_no', 'state')
        current_task_dict = {i['end_location']: {'agv_no': i['agv_no'], 'state': i['state']} for i in current_tasks}

        if '1' not in dp_type_split:
            # 站台信息
            platform_data = PlatFormInfo.objects.filter(
                **pf_f_kwargs).values(
                'id', 'desc', 'platform_real_info__state', 'location_name', 'platform_real_info__is_connected',
                'platform_real_info__upper_rail_state', 'process__process_name',
                'platform_real_info__lower_rail_state', 'platform_real_info__upper_basket_num',
                'platform_real_info__lower_basket_num', 'is_used', 'process__upper_rail_type',
                'process__lower_rail_type', 'task_trigger_type', 'up_task_trigger_threshold',
                'down_task_trigger_threshold').order_by('platform_ID')

            for item in platform_data:
                desc = item['desc']
                process_name = item['process__process_name']
                state = item['platform_real_info__state']
                location_name = item['location_name']
                is_used = item['is_used']
                task_trigger_type = item['task_trigger_type']
                upper_rail_type = item['process__upper_rail_type']
                lower_rail_type = item['process__lower_rail_type']
                up_task_trigger_threshold = item['up_task_trigger_threshold']
                down_task_trigger_threshold = item['down_task_trigger_threshold']
                up_basket_num = item['platform_real_info__upper_basket_num']  # 上料花篮数
                down_basket_num = item['platform_real_info__lower_basket_num']  # 下料花篮数
                up_rail_state = item['platform_real_info__upper_rail_state']  # 上料屏蔽
                down_rail_state = item['platform_real_info__lower_rail_state']  # 下料屏蔽
                is_connected = item['platform_real_info__is_connected']
                if not is_connected:
                    platform_status = 0
                else:
                    if not is_used:
                        platform_status = 4
                    else:
                        platform_status = state_dict.get(state, 5)
                task_info = current_task_dict.get(location_name)
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
                upper_rail_state = lower_rail_state = upper_basket_num = lower_basket_num = upper_threshold = lower_threshold = None
                if upper_rail_type == 1:
                    upper_basket_num = up_basket_num
                    upper_rail_state = up_rail_state
                    if task_trigger_type == 1:
                        upper_threshold = up_task_trigger_threshold
                elif upper_rail_type == 2:
                    upper_basket_num = down_basket_num
                    upper_rail_state = down_rail_state
                    if task_trigger_type == 2:
                        upper_threshold = down_task_trigger_threshold
                if lower_rail_type == 1:
                    lower_basket_num = up_basket_num
                    lower_rail_state = up_rail_state
                    if task_trigger_type == 1:
                        lower_threshold = up_task_trigger_threshold
                elif lower_rail_type == 2:
                    lower_basket_num = down_basket_num
                    lower_rail_state = down_rail_state
                    if task_trigger_type == 2:
                        lower_threshold = down_task_trigger_threshold
                table_data[process_name].append(
                    {'dp_type': 1,
                     'instance_id': item['id'],
                     'instance_name': desc,
                     'upper_rail_num': upper_basket_num,
                     'lower_rail_num': lower_basket_num,
                     'task_trigger_type': task_trigger_type,
                     'upper_trigger_threshold': upper_threshold,
                     'lower_trigger_threshold': lower_threshold,
                     'agv_no': agv_no,
                     'task_state': task_status,
                     'plt_state': platform_status,
                     'lower_rail_state': upper_rail_state,
                     'upper_rail_state': lower_rail_state,
                     'alarm_flag': None
                     }
                )

        if '2' not in dp_type_split:
            # 堆栈信息
            cache_devices = CacheDeviceRouteRelation.objects.filter(**dc_f_kwargs).values(
                'cache_device_id', 'cache_device__in_is_used', 'cache_device__device_name', 'cache_device__desc',
                'cache_device__in_location_name', 'cache_device__out_location_name', 'cache_device__row_num',
                'cache_device__column_num', 'cache_device__layer_num', 'cache_device__out_is_used',
                'group__process__process_name', 'group__process__process_ID', 'cache_device__is_connected').order_by('cache_device__device_name')
            stock_info = dict(CacheDeviceStock.objects.filter(
                basket_num__gt=0).values('equip_code').annotate(cnt=Count('id')).values_list('equip_code', 'cnt'))
            stock_platform_group_info = CacheDeviceStock.objects.filter(
                basket_num__gt=0).values('equip_code', 'in_processID').annotate(cnt=Count('id'))
            stock_platform_group_dict = {'{}-{}'.format(i['in_processID'], i['equip_code']): i['cnt'] for i in stock_platform_group_info}
            for device in cache_devices:
                process_name = device['group__process__process_name']
                process_ID = device['group__process__process_ID']
                cache_device_id = device['cache_device_id']
                device_name = device['cache_device__device_name']
                device_desc = device['cache_device__desc']
                in_location_name = device['cache_device__in_location_name']
                out_location_name = device['cache_device__out_location_name']
                in_is_used = device['cache_device__in_is_used']
                out_is_used = device['cache_device__out_is_used']
                row_num = device['cache_device__row_num']
                column_num = device['cache_device__column_num']
                layer_num = device['cache_device__layer_num']
                is_connected = device['cache_device__is_connected']
                in_task_info = current_task_dict.get(in_location_name)
                out_task_info = current_task_dict.get(out_location_name)
                in_agv_no = in_task_status = out_agv_no = out_task_status = None
                if in_task_info:
                    in_agv_no = in_task_info.get('agv_no')
                    in_task_state = in_task_info.get('state')
                    if in_task_state in (1, 2):
                        in_task_status = 1
                    elif in_task_state == 3:
                        in_task_status = 2
                    elif in_task_state == 4:
                        in_task_status = 3
                    else:
                        in_task_status = 4
                if out_task_info:
                    out_agv_no = out_task_info.get('agv_no')
                    out_task_state = out_task_info.get('state')
                    if out_task_state in (1, 2):
                        out_task_status = 1
                    elif out_task_state == 3:
                        out_task_status = 2
                    elif out_task_state == 4:
                        out_task_status = 3
                    else:
                        out_task_status = 4
                table_data[process_name].append(
                    {'dp_type': 2,  # 类型 1：站台 2：堆栈 3：缓存位
                     'instance_id': cache_device_id,  # 数据库id
                     'instance_name': device_desc,  # 名称
                     'up_agv_no': in_agv_no,  # 上料口AGV车号
                     'down_agv_no': out_agv_no,  # 下料口AGV车号
                     'up_task_state': in_task_status,  # 上料口任务状态 1：已创建 2：已下发 3：已派车 4：已到达
                     'down_task_state': out_task_status,  # 下料口任务状态 1：已创建 2：已下发 3：已派车 4：已到达
                     'in_plt_state': 1 if in_is_used else 4,  # 机台状态 1：正常生产 2：缺料 3：故障 4：已屏蔽 5：其他
                     'out_plt_state': 1 if out_is_used else 4,  # 机台状态 1：正常生产 2：缺料 3：故障 4：已屏蔽 5：其他
                     'in_is_used': in_is_used,
                     'out_is_used': out_is_used,
                     'is_connected': is_connected,
                     'total_locations': row_num * column_num * layer_num,  # 总库位数
                     'used_locations': stock_info.get(device_name, 0),  # 已占用库位数
                     'process_used_locations': stock_platform_group_dict.get('{}-{}'.format(process_ID, device_name), 0)  # 当前工艺段已占用库位数
                     })

        # if '3' not in dp_type_split:
        #     # 休息位信息
        #     rest_locations = RestLocationRouteRelation.objects.values(
        #         'rest_location_id', 'group__route_schema__route_name',
        #         'rest_location__location_name', 'group__process__process_name').order_by('rest_location__location_name')
        #     for rl in rest_locations:
        #         route_name = rl['group__route_schema__route_name']
        #         process_name = rl['group__process__process_name']
        #         lc_name = rl['rest_location__location_name']
        #         table_data[route_name][process_name].append(
        #             {'dp_type': 3,
        #              'instance_name': lc_name,
        #              'agv_no': None,
        #              }
        #         )
        return Response({'table_head': table_head, 'table_data': table_data})


@method_decorator([api_recorder], name="dispatch")
class RealTimeView(APIView):

    def get(self, request):
        params = self.request.query_params
        f_platform_ID = params.get('platform_ID')
        f_platform_name = params.get('platform_name')
        f_basket_num = params.get('basket_num')
        f_task_status = params.get('task_status')
        f_action = params.get('action')
        f_update_time = params.get('update_time')
        f_is_used = params.get('is_used')
        f_server_status = params.get('server_status')
        f_ordering = params.get('ordering')
        page = params.get('page', 1)
        page_size = params.get('page_size', 10)
        ret = []
        query_set = PlatFormInfo.objects.values(
            'platform_ID', 'platform_name', 'task_trigger_type', 'is_used', 'location_name',
            'platform_real_info__upper_basket_num', 'platform_real_info__lower_basket_num',
            'platform_real_info__upper_basket_changed_time', 'platform_real_info__lower_basket_changed_time',
            'platform_real_info__upper_rail_state', 'platform_real_info__lower_rail_state',
            'platform_real_info__is_connected'
        ).order_by('process__ordering', 'platform_ID')
        current_tasks = Tasks.objects.filter(state__in=(1, 2, 3, 4, 5, 6)).values_list('end_location', flat=True)

        for item in query_set:
            platform_ID = item['platform_ID']
            platform_name = item['platform_name']
            is_used = item['is_used']
            location_name = item['location_name']
            task_trigger_type = item['task_trigger_type']
            upper_basket_num = item['platform_real_info__upper_basket_num']
            lower_basket_num = item['platform_real_info__lower_basket_num']
            upper_basket_changed_time = item['platform_real_info__upper_basket_changed_time']
            lower_basket_changed_time = item['platform_real_info__lower_basket_changed_time']
            is_connected = item['platform_real_info__is_connected']
            if task_trigger_type == 1:
                basket_num = upper_basket_num
                action = 'GET'
                update_time = upper_basket_changed_time
            elif task_trigger_type == 2:
                basket_num = lower_basket_num
                action = 'PUT'
                update_time = lower_basket_changed_time
            else:
                basket_num = ''
                action = ''
                update_time = ''
            ret.append(
                {'platform_ID': platform_ID,
                 'platform_name': platform_name,
                 'is_used': is_used,
                 'server_status': 1 if is_connected else 0,
                 'basket_num': '' if basket_num == '' else basket_num,
                 'task_status': 'T' if location_name in current_tasks else 'F',
                 'action': '' if not action else action,
                 'update_time': '' if not update_time else update_time.strftime('%Y-%m-%d %H:%M:%S')}
            )
        if f_platform_ID:
            ret = filter(lambda x: f_platform_ID in x['platform_ID'], ret)
        if f_platform_name:
            ret = filter(lambda x: f_platform_name in x['platform_name'], ret)
        if f_is_used:
            ret = filter(lambda x: int(f_is_used) == x['is_used'], ret)
        if f_server_status:
            ret = filter(lambda x: int(f_server_status) == x['server_status'], ret)
        if f_basket_num:
            ret = filter(lambda x: int(f_basket_num) == x['basket_num'], ret)
        if f_task_status:
            ret = filter(lambda x: f_task_status == x['task_status'], ret)
        if f_action:
            if f_action == '1':
                ret = filter(lambda x: x['action'] == 'PUT', ret)
            elif f_action == '2':
                ret = filter(lambda x: x['action'] == 'GET', ret)
        if f_update_time:
            ret = filter(lambda x: f_update_time in x['update_time'], ret)
        # 排序
        try:
            if f_ordering:
                ordering_list = f_ordering.split('-')
                s_field = ordering_list[-1]
                if len(ordering_list) == 2:
                    ret = sorted(ret, key=lambda x: x[s_field], reverse=True)
                else:
                    ret = sorted(ret, key=lambda x: x[s_field])
        except Exception as e:
            raise ValidationError('排序异常！')

        ret = list(ret)
        # 获取分页数据
        try:
            st = (int(page) - 1) * int(page_size)
            et = int(page) * int(page_size)
        except:
            raise ValidationError("page/page_size异常，请修正后重试")
        else:
            if st not in range(0, 99999):
                raise ValidationError("page/page_size值异常")
            if et not in range(0, 99999):
                raise ValidationError("page/page_size值异常")
        results = ret[st:et]
        all_page = math.ceil(len(ret) / int(page_size))
        return Response({'results': results, 'all_page': all_page, 'all_data': len(ret)})


@method_decorator([api_recorder], name="dispatch")
class InProcessView(APIView):

    def get(self, request):
        f_route_name = request.query_params.get('route_name')
        process_filter, task_filter, stock_filter = {}, {}, {}
        if f_route_name:
            process_filter['route_schema__route_name'] = f_route_name
            task_filter['route_name'] = f_route_name
            # 堆栈过滤
            stock_ids = CacheDeviceRouteRelation.objects.filter(group__route_schema__route_name=f_route_name).values('cache_device__device_ID')
            stock_filter['equip_code__in'] = stock_ids
        results, productions, agv_detail = {}, {}, {}
        # 所有下料工艺段
        processes_info = (ProcessSection.objects.filter().filter(Q(upper_rail_type=2) | Q(lower_rail_type=2)).order_by('ordering')
                          .values('process_name', 'cell_numbers', 'single_slot_num'))
        processes_cell, process_slot, result_temp, production_temp = {}, {}, {}, {}
        for p in processes_info:
            p_name = p['process_name']
            result_temp[p_name] = {'AGV': 0, 'WIP': 0, 'EQUIP': 0}
            production_temp[p_name] = 0
            processes_cell[p_name] = p['cell_numbers']
            process_slot[p_name] = p['single_slot_num']
        # 站台组信息
        group_process = PlatformGroup.objects.filter(group_type=1, route_schema__is_used=True, **process_filter).values('group_ID', 'route_schema__route_name', 'process__process_name')
        group_process_dict = {i['group_ID']: [i['route_schema__route_name'], i['process__process_name']] for i in group_process}
        # 所有卸料机台花篮数
        p_real = PlatFormRealInfo.objects.filter(platform_info__process__process_name__in=processes_cell.keys()) \
            .values('platform_info__group__route_schema__route_name', 'platform_info__process__process_name') \
            .annotate(all_basket=Sum('upper_basket_num')) \
            .values('platform_info__group__route_schema__route_name',
                    'platform_info__process__process_name',
                    'platform_info__group__group_ID',
                    'all_basket')
        p_real_dict = {i['platform_info__process__process_name']: [i['all_basket'] if i['all_basket'] else 0, i['platform_info__group__group_ID'], i['platform_info__group__route_schema__route_name']] for i in p_real}
        # 获取AGV实时在制
        agv_info = {}
        data, code = get_agv_info()
        if code == 200 and "code" in data and data["code"] == 0:
            success_list = data["data"]['data']
            for item in success_list:
                agv_id, g1_a, g2_a = item.get('agv_id'), item.get('G1A', {}).get('machine_group'), item.get('G2A', {}).get('machine_group')
                if g1_a:
                    machine_group = g1_a
                elif g2_a:
                    machine_group = g2_a
                else:
                    machine_group = None
                if machine_group:
                    machine_group_info = group_process_dict.get(machine_group)
                    if machine_group_info:
                        machine_group_process = machine_group_info[1]
                        keyword = f"{machine_group}_{machine_group_process}"
                        basket_num = process_slot.get(machine_group_process, 5) * 2 if p_real_dict.get(machine_group_process, [0, 0, ''])[1] == machine_group else 0
                        agv_info[keyword] = {'process_num': agv_info.get(keyword, {}).get('process_num', 0) + basket_num,
                                             'agv': agv_info.get(keyword, {}).get('agv', []) + [agv_id]}
        # 获取任务数
        now = datetime.datetime.now()
        if 8 <= now.hour < 20:
            st, et = now.strftime('%Y-%m-%d 08:00:00'), now.strftime('%Y-%m-%d 20:00:00')
        else:
            st, et = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d 20:00:00'), now.strftime('%Y-%m-%d 08:00:00')
        # 累计产量
        tasks = Tasks.objects.filter(task_type__in=[2, 4], state=7, end_time__gte=st, end_time__lte=et, task_location_type=1, **task_filter) \
            .values('route_name', 'process_name').annotate(num=Count('id')).values('route_name', 'process_name', 'num')
        task_dict = {f"{t['route_name']}_{t['process_name']}": t['num'] for t in tasks}
        # 堆栈数据
        stock_data = dict(CacheDeviceStock.objects.filter(in_material_type_name__isnull=False, **stock_filter).values('in_material_type_name').annotate(num=Sum('basket_num')).values_list('in_material_type_name', 'num'))
        # 获取AGV实时在制
        for g_id, name_p in group_process_dict.items():
            route_name, process_name = name_p
            if process_name not in processes_cell:
                continue
            # 片改篮数
            cell = 1
            _p_info = agv_info.get(f"{g_id}_{process_name}", {})
            process_num, agv = [0, []] if not _p_info else [_p_info.get('process_num', 0) * cell, _p_info.get('agv', [])]
            equip_num = (p_real_dict.get(process_name)[0] * cell) if p_real_dict.get(process_name, [1, 0, ''])[-1] == route_name else 0
            wip_num = stock_data.get(g_id, 0) * cell
            if route_name not in results:
                if '合计' not in results:
                    _all_process = deepcopy(result_temp)
                    _all_process.update({process_name: {'AGV': process_num, 'WIP': wip_num, 'EQUIP': equip_num}, 'route_name': '合计'})
                    results['合计'] = _all_process
                else:
                    results['合计'][process_name].update({'AGV': results['合计'][process_name]['AGV'] + process_num,
                                                          'WIP': results['合计'][process_name]['WIP'] + wip_num,
                                                          'EQUIP': results['合计'][process_name]['EQUIP'] + equip_num})
                all_process = deepcopy(result_temp)
                all_process.update({process_name: {'AGV': process_num, 'WIP': wip_num, 'EQUIP': equip_num}, 'route_name': route_name})
                results[route_name] = all_process
            else:
                results['合计'][process_name].update({'AGV': results['合计'][process_name]['AGV'] + process_num,
                                                      'WIP': results['合计'][process_name]['WIP'] + wip_num,
                                                      'EQUIP': results['合计'][process_name]['EQUIP'] + equip_num})
                results[route_name][process_name].update({'AGV': results[route_name][process_name]['AGV'] + process_num,
                                                          'WIP': results[route_name][process_name]['WIP'] + wip_num,
                                                          'EQUIP': results[route_name][process_name]['EQUIP'] + equip_num})
            # 历史产量
            history_cell = processes_cell.get(process_name, 1160)
            num = task_dict.get(f"{route_name}_{process_name}", 0) * history_cell
            if route_name not in productions:
                if '合计' not in productions:
                    _p_process = deepcopy(production_temp)
                    _p_process.update({process_name: num, 'route_name': '合计'})
                    productions['合计'] = _p_process
                else:
                    hj_product = productions['合计'][process_name]
                    productions['合计'][process_name] = hj_product + num
                p_process = deepcopy(production_temp)
                p_process.update({process_name: num, 'route_name': route_name})
                productions[route_name] = p_process
            else:
                hj_product = productions['合计'][process_name]
                p_product = productions[route_name][process_name]
                productions['合计'][process_name] = hj_product + num
                productions[route_name][process_name] = p_product + num
            # agv详情
            if agv:
                agv_detail[process_name] = list(set(agv_detail.get(process_name, []) + agv))
        sorted_agv_detail = {key: sorted(value, key=lambda x: x) for key, value in agv_detail.items()}
        return Response({'results': results.values(), 'productions': productions.values(), 'agv_detail': sorted_agv_detail})


@method_decorator([api_recorder], name="dispatch")
class AgvInProcessView(APIView):

    def get(self, request):
        process = request.query_params.get('process')
        filter_kwargs = {}
        if process:
            filter_kwargs['id'] = process
        # 所有下料工艺段
        processes = ProcessSection.objects.filter(**filter_kwargs).filter(
            Q(upper_rail_type=2) | Q(lower_rail_type=2)).order_by('ordering').values_list('process_name', flat=True)
        group_process_dict = dict(PlatformGroup.objects.values_list('group_ID', 'process__process_name'))
        results = {p: {'process_name': p, 'total_belt': 0, 'free_agv': 0, 'all_agv_list': set(), 'free_agv_list': set()} for p in processes}
        # 获取AGV实时在制
        data, code = get_agv_info()
        if code == 200 and "code" in data and data["code"] == 0:
            success_list = data["data"]['data']
            for item in success_list:
                busy, agv_id, g1_a, g2_a = item.get('busy'), item.get('agv_id'), item.get('G1A', {}).get('machine_group'), item.get('G2A', {}).get('machine_group')
                if g1_a:
                    machine_group = g1_a
                elif g2_a:
                    machine_group = g2_a
                else:
                    machine_group = None
                if machine_group:
                    machine_group_process = group_process_dict.get(machine_group)
                    if machine_group_process in results:
                        results[machine_group_process]['total_belt'] += 1
                        results[machine_group_process]['all_agv_list'].add(agv_id)
                        if not busy:
                            results[machine_group_process]['free_agv'] += 1
                            results[machine_group_process]['free_agv_list'].add(agv_id)
        return Response({'results': results.values()})


@method_decorator([api_recorder], name="dispatch")
class InProcessTrendView(APIView):

    def get(self, request):
        route_name = self.request.query_params.get('route_name')
        process_name = self.request.query_params.get('process_name')
        try:
            default_hour = int(self.request.query_params.get('default_hour', 12))
        except:
            default_hour = 12
        filter_kwargs = {}
        if route_name:
            filter_kwargs['route_name'] = route_name
        if process_name:
            filter_kwargs['process_name'] = process_name
        now_time = datetime.datetime.now().replace(microsecond=0, second=0)
        n_minutes = now_time.minute
        handle_now_time = now_time - datetime.timedelta(minutes=n_minutes % 10)
        before_time = handle_now_time - datetime.timedelta(hours=default_hour)
        stock_dict, title, agv, wip = {}, [], [], []
        stock_info = (StockHistorySummary.objects.filter(created_time__gte=before_time, created_time__lte=now_time, **filter_kwargs).values('created_time')
                      .annotate(agv_num=Sum('agv_trains_num'), wip_num=Sum('cache_trains_num')).values('created_time', 'agv_num', 'wip_num'))
        for item in stock_info:
            str_time = item['created_time'].strftime('%Y-%m-%d %H:%M:%S')
            stock_dict[str_time] = [item['agv_num'], item['wip_num']]
        for s_t in range(default_hour * 2 + 1):
            keyword = (before_time + datetime.timedelta(minutes=30 * s_t)).strftime('%Y-%m-%d %H:%M:%S')
            agv_num, wip_num = stock_dict.get(keyword, [0, 0])
            agv.append(agv_num)
            wip.append(wip_num)
            title.append(keyword)
        return Response({'title': title, 'agv': agv, 'wip': wip})


@method_decorator([api_recorder], name="dispatch")
class AlarmView(ListAPIView):

    queryset = AlarmLog.objects.filter()
    serializer_class = AlarmSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = AlarmFilter
    ordering_fields = ('alarm_type', 'level', 'alarm_desc', 'alarm_times', 'last_updated_time')
    ordering = ('-last_updated_time',)


@method_decorator([api_recorder], name="dispatch")
class QTimeReportView(APIView):
    def get(self, request):
        # 工艺段电池片数量
        process_cells = dict(ProcessSection.objects.filter().values_list('process_ID', 'cell_numbers'))
        cache_data = CacheDeviceStock.objects.filter().values('equip_code', 'in_processID') \
            .annotate(total_basket=Sum('basket_num'),
                      expire_basket=Sum('basket_num', filter=Q(output_time_consume__gt=F('q_time')))).order_by('equip_code')
        data = {}
        for c in cache_data:
            cells = process_cells.get(c['in_processID'], 1160)
            equip_code, total_basket, expire_basket = c['equip_code'], c['total_basket'] * cells, 0 if not c['expire_basket'] else (c['expire_basket'] * cells)
            if equip_code not in data:
                data[equip_code] = {'equip_code': equip_code, 'expire_basket': expire_basket, 'total_basket': total_basket}
            else:
                data[equip_code]['expire_basket'] += expire_basket
                data[equip_code]['total_basket'] += total_basket
        # 补充比数据
        for i in data.values():
            expire_basket, total_basket = i['expire_basket'], i['total_basket']
            expire_ratio = round(expire_basket / total_basket * 100, 2) if total_basket else 0
            effective_ratio = round((total_basket - expire_basket) / total_basket * 100 , 2) if total_basket else 0
            i.update({'expire_ratio': expire_ratio, 'effective_ratio': effective_ratio})
        return Response(data.values())


@method_decorator([api_recorder], name="dispatch")
class TaskDurationReportView(APIView):
    def get(self, request):
        params = self.request.query_params
        page = params.get('page', 1)
        page_size = params.get('page_size', 10)
        platform_id = params.get('platform_ID')
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        filter_kwargs, filter_kwargs2 = {}, {}
        if platform_id:
            filter_kwargs['platform_ID'] = platform_id
            filter_kwargs2['platform_ID'] = platform_id
        if start_time:
            filter_kwargs['end_time__gte'] = start_time
        if end_time:
            filter_kwargs['end_time__lte'] = end_time
        # 获取所有的站台数据
        platform_info = PlatFormInfo.objects.filter(**filter_kwargs2).values('platform_ID', 'platform_name', 'process__process_name', 'process__process_ID').order_by('process', 'platform_ID')
        # 获取任务数据
        tasks = Tasks.objects.filter(state=7, task_location_type=1, **filter_kwargs).values('process_name', 'platform_ID') \
            .annotate(task=Count('id'), mean_task=Avg(F('end_time') - F('created_time'), output_field=DurationField()), mean_allot=Avg(F('bind_time') - F('active_time'), output_field=DurationField()),
                      mean_move=Avg(F('arrived_time') - F('dispatched_time'), output_field=DurationField()), mean_dock=Avg(F('end_time') - F('begin_act_time'), output_field=DurationField())) \
            .values('process_name', 'platform_ID', 'task', 'mean_task', 'mean_allot', 'mean_move', 'mean_dock').order_by('process_name', 'platform_ID')
        task_dict = {f"{task['process_name']}-{task['platform_ID']}": task for task in tasks}
        for p in platform_info:
            _task_info = task_dict.get(f"{p['process__process_name']}-{p['platform_ID']}")
            if not _task_info:
                _task_info = {'task': 0, 'mean_task': 0, 'mean_allot': 0, 'mean_move': 0, 'mean_dock': 0}
            else:
                # 转换数据
                _task_info['mean_task'] = round(_task_info['mean_task'].total_seconds(), 2) if _task_info['mean_task'] else 0
                _task_info['mean_allot'] = round(_task_info['mean_allot'].total_seconds(), 2) if _task_info['mean_allot'] else 0
                _task_info['mean_move'] = round(_task_info['mean_move'].total_seconds(), 2) if _task_info['mean_move'] else 0
                _task_info['mean_dock'] = round(_task_info['mean_dock'].total_seconds(), 2) if _task_info['mean_dock'] else 0
            p.update(_task_info)
        # 获取分页数据
        try:
            st = (int(page) - 1) * int(page_size)
            et = int(page) * int(page_size)
        except:
            raise ValidationError("page/page_size异常，请修正后重试")
        else:
            if st not in range(0, 99999):
                raise ValidationError("page/page_size值异常")
            if et not in range(0, 99999):
                raise ValidationError("page/page_size值异常")
        results = platform_info[st:et]
        all_page = math.ceil(len(platform_info) / int(page_size))
        return Response({'results': results, 'all_page': all_page, 'all_data': len(platform_info)})
