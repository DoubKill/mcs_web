import datetime
import logging

from django.db.models import Count, Max
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from agv.filters import EquipTaskTrackFilter, EnvCheckLocationsOrderingFilter, EnvCheckLocationsFilter, \
    EnvCheckTasksFilter, EnvLocationCheckHistoryFilter
from agv.models import Tasks, EnvIndicators, EnvCheckLocations, EnvCheckTasks, EnvLocationCheckHistory, \
    EnvTaskLocationRelation
from agv.serializers import EquipTaskTrackSerializer, EnvCheckLocationsSerializer, EnvCheckTasksSerializer, \
    EnvLocationCheckHistorySerializer
from basics.management.tasks.env_check import issue_task, create_task
from basics.models import ProcessSection, Configuration, PlatFormInfo
from mcs.common_code import CommonExportListMixin, CommonBatchDestroyView, gen_template_response
from mcs.derorators import api_recorder
from monitor.utils import cancel_cache_device_task
api_log = logging.getLogger('api_log')


@method_decorator([api_recorder], name="dispatch")
class RCSOrderTracebackView(APIView):
    # 订单状态： ["waiting", "active", "dispatched", "bind_agv", "interaction_request",
    #        "interaction_begin", "waiting_cancel", "finish", "cancel_finish", "error"]

    STATUS_MAPPING = {
        'active': {'state': 3, 'attr': 'active_time'},
        'dispatched': {'state': 3, 'attr': 'dispatched_time'},
        'bind_agv': {'state': 4, 'attr': 'bind_time'},
        'interaction_request': {'state': 5, 'attr': 'arrived_time'},
        'interaction_begin': {'state': 6, 'attr': 'begin_act_time'},
        'finish': {'state': 7, 'attr': 'end_time'},
        'error': {'state': 8, 'attr': 'error_time'},
        'cancel_finish': {'state': 9, 'attr': 'end_time'}
    }

    def post(self, request):
        # TODO 将订单反馈内容写入机台
        data = self.request.data
        order_status = data.get('orderStatus', '').strip()  # RCS订单状态
        task_no = data.get('orderName', '').strip()  # 订单号
        status_change_time = data.get('StatusChangeTime')  # RCS状态时间
        agv_no = data.get('agvIDList')  # AGV车号
        rcs_order_id = data.get('orderID')
        update_kwargs = {}
        try:
            task = Tasks.objects.get(task_no=task_no)
        except Tasks.DoesNotExist:
            return Response({"code": 1, "msg": '该任务号不存在'})
        if order_status in self.STATUS_MAPPING:
            mapping = self.STATUS_MAPPING[order_status]
            update_kwargs['state'] = mapping['state']
            update_kwargs[mapping['attr']] = status_change_time
            update_kwargs['rcs_order_id'] = rcs_order_id
            try:
                agv_no = int(agv_no)
            except ValueError:
                pass
            else:
                update_kwargs['agv_no'] = agv_no
                if order_status == 'finish':
                    kps = list(ProcessSection.objects.filter(
                        source_process__isnull=True).values_list('process_name', flat=True))
                    # 站台任务,且进料类型不是空车 或 堆栈进料任务，补充来源站台信息
                    if (task.task_location_type == 1 and task.process_name not in kps) or \
                            (task.task_location_type == 2 and task.task_type == 3):
                        last_order = Tasks.objects.filter(state=7, agv_no=agv_no).order_by('end_time').last()
                        if last_order:
                            update_kwargs['origin_platform_ID'] = last_order.platform_ID
                            update_kwargs['origin_platform_name'] = last_order.platform_name
                            update_kwargs['receive_time'] = last_order.end_time
                elif order_status == 'cancel_finish' and task.task_location_type == 2:
                    resp_data, recode = cancel_cache_device_task(task.end_location, 'in' if task.task_type == 3 else 'out', task.dz_group_no)
                    if recode == 200:
                        api_log.info('堆栈任务：{},取消成功！'.format(task.task_no))
                    else:
                        api_log.error('堆栈任务：{},取消失败，返回信息：{}'.format(task.task_no, resp_data))
        else:
            return Response({"code": 0, "msg": 'success'})
        Tasks.objects.filter(task_no=task_no).update(**update_kwargs)
        return Response({"code": 0, "msg": 'success'})


@method_decorator([api_recorder], name="dispatch")
class ProductivityStatisticsView(APIView):
    """产能统计"""

    def get(self, request):
        st = self.request.query_params.get('st')
        et = self.request.query_params.get('et')
        filter_kwargs = {'task_location_type': 1, 'state': 7}
        if st:
            filter_kwargs['end_time__gte'] = st
        if et:
            filter_kwargs['end_time__lte'] = et
        ret = []
        process_data = ProcessSection.objects.values(
            'process_name', 'upper_rail_type', 'upper_basket_type',
            'lower_rail_type', 'lower_basket_type', 'cell_numbers').order_by('ordering')
        query_data_dict = dict(Tasks.objects.filter(
            **filter_kwargs).values('process_name').annotate(cnt=Count('id')).values_list('process_name', 'cnt'))
        for item in process_data:
            process_name = item['process_name']
            upper_rail_type = item['upper_rail_type']
            upper_basket_type = item['upper_basket_type']
            lower_rail_type = item['lower_rail_type']
            lower_basket_type = item['lower_basket_type']
            cell_numbers = item['cell_numbers']
            task_cnt = query_data_dict.get(process_name, 0)
            in_basket_num = out_basket_num = 0
            if upper_rail_type == 1:
                if upper_basket_type in (1, 3, 5):
                    in_basket_num = 0
                else:
                    in_basket_num = task_cnt * cell_numbers
            elif upper_rail_type == 2:
                if upper_basket_type in (1, 3, 5):
                    out_basket_num = 0
                else:
                    out_basket_num = task_cnt * cell_numbers

            if lower_rail_type == 1:
                if lower_basket_type in (1, 3, 5):
                    in_basket_num = 0
                else:
                    in_basket_num = task_cnt * cell_numbers
            elif lower_rail_type == 2:
                if lower_basket_type in (1, 3, 5):
                    out_basket_num = 0
                else:
                    out_basket_num = task_cnt * cell_numbers
            ret.append({
                'process_name': process_name,
                'in_basket_num': in_basket_num,
                'out_basket_num': out_basket_num
            })
        return Response({'data': ret})


@method_decorator([api_recorder], name="dispatch")
class EquipProductivityStatisticsView(APIView):
    """机台产能统计"""

    def get(self, request):
        st = self.request.query_params.get('st')
        et = self.request.query_params.get('et')
        q_platform_name = self.request.query_params.get('platform_name')
        q_process_name = self.request.query_params.get('process_name')
        filter_kwargs = {'task_location_type': 1, 'state': 7}
        p_kwargs = {}
        if st:
            filter_kwargs['end_time__gte'] = st
        if et:
            filter_kwargs['end_time__lte'] = et
        if q_platform_name:
            filter_kwargs['platform_name'] = q_platform_name
            p_kwargs['platform_name'] = q_platform_name
        if q_process_name:
            filter_kwargs['process_name'] = q_process_name
            p_kwargs['process__process_name'] = q_process_name
        ret = []
        platform_data = PlatFormInfo.objects.filter(**p_kwargs).values(
            'platform_name', 'process__upper_rail_type', 'process__upper_basket_type',
            'process__lower_rail_type', 'process__lower_basket_type', 'process__cell_numbers', 'process__process_name'
        ).order_by('process__ordering', 'platform_name')
        query_data_dict = dict(Tasks.objects.filter(
            **filter_kwargs).values('platform_name').annotate(cnt=Count('id')).values_list('platform_name', 'cnt'))
        for item in platform_data:
            platform_name = item['platform_name']
            upper_rail_type = item['process__upper_rail_type']
            upper_basket_type = item['process__upper_basket_type']
            lower_rail_type = item['process__lower_rail_type']
            lower_basket_type = item['process__lower_basket_type']
            cell_numbers = item['process__cell_numbers']
            process_name = item['process__process_name']
            task_cnt = query_data_dict.get(platform_name, 0)
            in_basket_num = out_basket_num = 0
            if upper_rail_type == 1:
                if upper_basket_type in (1, 3, 5):
                    in_basket_num = 0
                else:
                    in_basket_num = task_cnt * cell_numbers
            elif upper_rail_type == 2:
                if upper_basket_type in (1, 3, 5):
                    out_basket_num = 0
                else:
                    out_basket_num = task_cnt * cell_numbers

            if lower_rail_type == 1:
                if lower_basket_type in (1, 3, 5):
                    in_basket_num = 0
                else:
                    in_basket_num = task_cnt * cell_numbers
            elif lower_rail_type == 2:
                if lower_basket_type in (1, 3, 5):
                    out_basket_num = 0
                else:
                    out_basket_num = task_cnt * cell_numbers
            ret.append({
                'process_name': process_name,
                'platform_name': platform_name,
                'in_basket_num': in_basket_num,
                'out_basket_num': out_basket_num
            })
        return Response({'data': ret})


@method_decorator([api_recorder], name="dispatch")
class StationTaskTrackView(ListAPIView):
    queryset = Tasks.objects.filter(state=7, task_location_type=1).order_by('-id')
    serializer_class = EquipTaskTrackSerializer
    filter_class = EquipTaskTrackFilter
    filter_backends = (DjangoFilterBackend, )


@method_decorator([api_recorder], name="dispatch")
class EnvIndicatorsView(APIView):

    def get(self, request):
        if not EnvIndicators.objects.filter().exists():
            ret = []
            for i in range(1, 8):
                ret.append({'indicator_type': i, 'warning_value': None, 'alarm_value': None})
            return Response(ret)
        return Response(EnvIndicators.objects.values(
            'indicator_type', 'warning_value', 'alarm_value').order_by('indicator_type'))

    def post(self, request):
        data = self.request.data
        for item in data:
            indicator_type = item['indicator_type']
            warning_value = item['warning_value']
            alarm_value = item['alarm_value']
            kwargs = {'indicator_type': indicator_type}
            defaults = {'warning_value': warning_value, 'alarm_value': alarm_value}
            EnvIndicators.objects.update_or_create(defaults=defaults, **kwargs)
        return Response('OK')


@method_decorator([api_recorder], name="dispatch")  # 本来是删除，现在改为是启用就改为禁用 是禁用就改为启用
class EnvCheckLocationsViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = EnvCheckLocations.objects.all()
    serializer_class = EnvCheckLocationsSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = EnvCheckLocationsFilter
    filter_backends = (DjangoFilterBackend, EnvCheckLocationsOrderingFilter)
    ordering_fields = ('location_name', 'working_area', 'created_username', 'created_time', 'last_updated_time', 'last_updated_username')
    ordering = ('location_name',)
    VALUES_FIELDS = ['id', 'location_name', 'working_area']


@method_decorator([api_recorder], name="dispatch")  # 本来是删除，现在改为是启用就改为禁用 是禁用就改为启用
class EnvCheckTasksViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = EnvCheckTasks.objects.all()
    serializer_class = EnvCheckTasksSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = EnvCheckTasksFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('task_no', 'task_name', 'working_area', 'task_trigger_type', 'check_location_name', 'is_used')
    ordering = ('task_no',)
    VALUES_FIELDS = ['id', 'task_no', 'task_name', 'working_area']

    @action(methods=['post'], detail=False, url_path='issue-task', url_name='issue-task')
    def issue_task(self, request):
        task_id = self.request.data.get('task_id')
        t = EnvCheckTasks.objects.get(id=task_id)
        now_time = datetime.datetime.now()
        check_no = '{}{}'.format(t.task_no, now_time.strftime('%Y%m%d%H%M%S'))
        location_names = list(EnvTaskLocationRelation.objects.filter(
            check_task=t).values_list('check_location__location_name', flat=True).order_by('ordering'))
        rcs_url = Configuration.objects.get(key='rcs_url').value
        success_flag = issue_task(rcs_url, check_no, location_names)
        if success_flag:
            state = 1
        else:
            state = 0
        create_task(check_no, t.task_no, t.working_area.area_name, location_names, state)
        return Response('OK')


@method_decorator([api_recorder], name="dispatch")
class EnvLocationCheckHistoryView(CommonExportListMixin, ListAPIView):
    queryset = EnvLocationCheckHistory.objects.order_by('-id')
    serializer_class = EnvLocationCheckHistorySerializer
    filter_class = EnvLocationCheckHistoryFilter
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, )
    EXPORT_FIELDS_DICT = {
        '检测点名称': 'location_name',
        '检测任务编号': 'task_no',
        '所属工作区': 'working_area_name',
        '小车号': 'agv_no',
        '创建时间': 'created_time',
        '上报时间': 'report_time',
        '温度': 'indicator_value_1',
        '湿度': 'indicator_value_2',
        '0.3微米离子数': 'indicator_value_3',
        '0.5微米离子数': 'indicator_value_4',
        '1微米离子数': 'indicator_value_5',
        '3微米离子数': 'indicator_value_6',
        '5微米离子数': 'indicator_value_7'
    }
    FILE_NAME = '环境检测报表.xlsx'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        export = self.request.query_params.get('export')
        new_flag = self.request.query_params.get('new_flag')
        if new_flag:
            q_ids = list(EnvLocationCheckHistory.objects.values(
                'location_name').annotate(max_id=Max('id')).values_list('max_id', flat=True))
            queryset = queryset.filter(id__in=q_ids)
        if export:
            data = self.get_serializer(queryset, many=True).data
            return gen_template_response(self.EXPORT_FIELDS_DICT, data, self.FILE_NAME,
                                         self.SHEET_NAME, self.TEMPLATE_FILE)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@method_decorator([api_recorder], name="dispatch")
class EnvCheckResultTraceback(APIView):
    # {
    #     "check_no": '111',  # 检查编号
    #     "location_name": "a",
    #     "check_time": "2022-11-11 12:12:12",  # 检查时间
    #     "agv_no": 1,  # AGV
    #     "indicator_value_1": 1,  # 温度
    #     "indicator_value_2": 1,  # 湿度
    #     "indicator_value_3": 1,  # 0.3微米离子数
    #     "indicator_value_4": 1,  # 0.5微米离子数
    #     "indicator_value_5": 1,  # 1微米离子数
    #     "indicator_value_6": 1,  # 3微米离子数
    #     "indicator_value_7": 1,  # 5微米离子数
    # }
    authentication_classes = ()

    def post(self, request):
        data = self.request.data
        check_no = data.get('check_no', '').strip()  # RCS订单状态
        location_name = data.get('location_name', '').strip()  # 订单号
        check_time = data.get('check_time')  # RCS状态时间
        agv_no = data.get('agv_no')  # AGV车号
        indicator_value_1 = data.get('indicator_value_1')
        indicator_value_2 = data.get('indicator_value_2')
        indicator_value_3 = data.get('indicator_value_3')
        indicator_value_4 = data.get('indicator_value_4')
        indicator_value_5 = data.get('indicator_value_5')
        indicator_value_6 = data.get('indicator_value_6')
        indicator_value_7 = data.get('indicator_value_7')
        check_history = EnvLocationCheckHistory.objects.filter(
            check_no=check_no, location_name=location_name).first()
        env_valid_time = Configuration.objects.get(key='env_valid_time').value

        if check_history:
            indicator_warning_dict = dict((EnvIndicators.objects.values_list('indicator_type', 'warning_value')))
            indicator_alarm_dict = dict((EnvIndicators.objects.values_list('indicator_type', 'alarm_value')))
            check_history.state = 2
            check_history.agv_no = agv_no
            check_history.report_time = check_time
            check_history.indicator_value_1 = indicator_value_1
            check_history.indicator_value_2 = indicator_value_2
            check_history.indicator_value_3 = indicator_value_3
            check_history.indicator_value_4 = indicator_value_4
            check_history.indicator_value_5 = indicator_value_5
            check_history.indicator_value_6 = indicator_value_6
            check_history.indicator_value_7 = indicator_value_7
            if indicator_warning_dict and indicator_alarm_dict:
                if indicator_value_1 > indicator_alarm_dict[1] \
                        or indicator_value_2 > indicator_alarm_dict[2]\
                        or indicator_value_3 > indicator_alarm_dict[3]\
                        or indicator_value_4 > indicator_alarm_dict[4]\
                        or indicator_value_5 > indicator_alarm_dict[5]\
                        or indicator_value_6 > indicator_alarm_dict[6]\
                        or indicator_value_7 > indicator_alarm_dict[7]:
                    check_history.check_state = 3
                elif indicator_value_1 > indicator_warning_dict[1] \
                        or indicator_value_2 > indicator_warning_dict[2]\
                        or indicator_value_3 > indicator_warning_dict[3]\
                        or indicator_value_4 > indicator_warning_dict[4]\
                        or indicator_value_5 > indicator_warning_dict[5]\
                        or indicator_value_6 > indicator_warning_dict[6]\
                        or indicator_value_7 > indicator_warning_dict[7]:
                    check_history.check_state = 2
            if env_valid_time:
                now_time = datetime.datetime.now()
                time_diff = (now_time - datetime.datetime.strptime(check_time.split('.')[0], '%Y-%m-%d %H:%M:%S')).total_seconds()
                if time_diff > int(env_valid_time) * 60:
                    check_history.is_useful = False
            check_history.save()
        return Response({"code": 0, "msg": 'success'})