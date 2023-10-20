import json
import logging
import math
import datetime
import os

from django.db.models import Max, F, Value, IntegerField, Q, ProtectedError
from django.db.transaction import atomic
from django.http import FileResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from agv.models import CacheDeviceStock, Tasks
from mcs.common_code import CommonBatchDestroyView, CommonExportListMixin, get_cur_sheet, get_sheet_data, \
    gen_template_response
from mcs.derorators import api_recorder
from basics.filters import GlobalCodeTypeFilter, GlobalCodeFilter, ProcessSectionFilter, PlatFormInfoFilter, \
    RestLocationFilter, PlatformGroupFilter, CacheDeviceInfoFilter, WorkAreaFilter, PlatFormInfoOrderingFilter, \
    RestLocationOrderingFilter, CacheDeviceInfoOrderingFilter, LocationOrderingFilter, LocationFilter, \
    LocationGroupFilter, ThresholdDisplayFilter
from basics.models import GlobalCodeType, GlobalCode, ProcessSection, PlatFormInfo, RestLocation, RoutingSchema, \
    CacheDeviceRouteRelation, RestLocationRouteRelation, \
    PlatformGroup, CacheDeviceInfo, EmptyBasketRouteSchema, WorkArea, Configuration, ProcessCacheDeviceRelation, \
    EmptyCacheRouteSchema, CacheDevicePreRouteRelation, Location, LocationGroup, PlatFormRealInfo, PlatformPart, AgvType
from basics.serializers import GlobalCodeTypeSerializer, GlobalCodeSerializer, ProcessSectionSerializer, \
    PlatFormInfoSerializer, PlatFormInfoUpdateSerializer, RestLocationSerializer, RoutingSchemaSerializer, \
    PlatformGroupSerializer, CacheDeviceInfoSerializer, CacheDeviceInfoUpdateSerializer, LocationSerializer, \
    WorkAreaSerializer, PlatFormInfoCreateSerializer, RoutingSchemaUpdateSerializer, LocationGroupSerializer, \
    ThresholdDisplaySerializer, PlatFormImportSerializer, PlatFormExportSerializer, AgvTypeSerializer
from monitor.utils import get_rest_locations, cancel_task
from user.models import GroupExtension

e_logger = logging.getLogger('error_log')


@method_decorator([api_recorder], name="dispatch")
class CommonCodeView(APIView):

    def get(self, request):
        code = self.request.query_params.get('code')
        if code == '1':
            prefix, model_name = ['T', GlobalCodeType]
            max_code = model_name.objects.filter(
                type_no__startswith=prefix).aggregate(max_code=Max('type_no'))['max_code']
        elif code == '2':
            prefix, model_name = ['C', GlobalCode]
            max_code = model_name.objects.filter(
                global_no__startswith=prefix).aggregate(max_code=Max('global_no'))['max_code']
        elif code == '5':
            prefix, model_name = ['R', GroupExtension]
            max_code = model_name.objects.filter(
                group_code__startswith=prefix).aggregate(max_code=Max('group_code'))['max_code']
        else:
            raise ValidationError('参数错误')
        try:
            if not max_code:
                default_code = f'{prefix}00001'
            else:
                s = len(prefix)
                default_code = '{}{:05}'.format(prefix, int(max_code[s:]) + 1)
        except Exception:
            raise ValidationError('解析自增公共编码异常')
        return Response(data={'results': default_code})


@method_decorator([api_recorder], name="dispatch")
class GlobalCodeTypeViewSet(CommonBatchDestroyView, ModelViewSet):
    """
    list:
        公共代码类型列表
    create:
        创建公共代码类型
    update:
        修改公共代码类型
    destroy:
        删除公共代码类型
    """
    queryset = GlobalCodeType.objects.filter(delete_flag=False).order_by("type_no")
    serializer_class = GlobalCodeTypeSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = GlobalCodeTypeFilter


@method_decorator([api_recorder], name="dispatch")  # 本来是删除，现在改为是启用就改为禁用 是禁用就改为启用
class GlobalCodeViewSet(CommonBatchDestroyView, ModelViewSet):
    """
    list:
        公共代码列表
    create:
        创建公共代码
    update:
        修改公共代码
    destroy:
        删除公共代码
    """
    queryset = GlobalCode.objects.filter(delete_flag=False).order_by("global_no")
    serializer_class = GlobalCodeSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    filter_class = GlobalCodeFilter


@method_decorator([api_recorder], name="dispatch")
class AgvTypeViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = AgvType.objects.all().order_by('type_ID')
    serializer_class = AgvTypeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    VALUES_FIELDS = ['id', 'type_ID', 'type_name']


@method_decorator([api_recorder], name="dispatch")
class WorkAreaViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = WorkArea.objects.all().order_by('id')
    serializer_class = WorkAreaSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    filter_class = WorkAreaFilter
    filter_backends = (DjangoFilterBackend,)
    VALUES_FIELDS = ['id', 'area_ID', 'area_name', 'rcs_address']


@method_decorator([api_recorder], name="dispatch")  # 本来是删除，现在改为是启用就改为禁用 是禁用就改为启用
class ProcessSectionViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = ProcessSection.objects.filter(delete_flag=False)
    serializer_class = ProcessSectionSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = ProcessSectionFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('process_ID', 'process_name', 'ordering', 'cell_numbers', 'q_time',
                       'pitch_time', 'working_area', 'source_process', 'target_process',
                       'upper_rail_type', 'upper_basket_type', 'lower_rail_type',
                       'lower_basket_type', 'pitch_time', 'single_slot_num')
    ordering = ['ordering']
    VALUES_FIELDS = ['id', 'process_name', 'ordering', 'upper_rail_type', 'lower_rail_type', 'q_time', 'pitch_time',
                     'working_area', 'upper_basket_type', 'lower_basket_type', 'source_process', 'target_process']
    EXPORT_FIELDS_DICT = {
        '工艺段ID': 'process_ID',
        '工艺段名称': 'process_name',
        '工艺段顺序': 'ordering',
        '源工艺段': 'source_process_name',
        '目标工艺段': 'target_process_name',
        '工作区': 'working_area_name',
        '上层轨道上下料类型': 'upper_rail_type_name',
        '上层花篮类型': 'upper_basket_type_name',
        '下层轨道上下料类型': 'lower_rail_type_name',
        '下层花篮类型': 'lower_basket_type_name',
        '单轴花篮数': 'single_slot_num',
        '物料超时时间(秒)': 'q_time',
        '单车电池片数量': 'cell_numbers',
        'QTime预警时间(秒)': 'q_time',
        '节拍(秒)': 'pitch_time',
    }
    FILE_NAME = '工艺段配置.xlsx'

    def generate_circle_layout(self, process_list, center_x, center_y, radius):
        data = []
        for i, process_name in enumerate(process_list):
            angle = (2 * math.pi * i) / len(process_list)
            x = round(center_x + radius * math.cos(angle))
            y = round(center_y + radius * math.sin(angle))
            point = {
                'name': process_name,
                'x': x,
                'y': y
            }
            data.append(point)
        return data

    @action(methods=['get'], detail=False, url_path='process-cyclic-graph', url_name='process_cyclic_graph')
    def process_cyclic_graph(self, request):
        try:
            params = self.request.query_params
            center_x, center_y, radius = params.get('center_x', 500), params.get('center_y', 300), params.get('radius', 200)
            links = []
            origin_data = self.get_queryset().order_by('working_area', 'ordering').annotate(area_name=F('working_area__area_name'),
                                                                                            source_name=F('source_process__process_name'),
                                                                                            target_name=F('target_process__process_name'),
                                                                                            target_ordering=F('target_process__ordering')) \
                .values('area_name', 'process_name', 'ordering', 'source_name', 'target_name', 'target_ordering')
            results, _area_process = {}, {}
            for o in origin_data:
                area_name, process_name, ordering, target_ordering, target_name = o['area_name'], o['process_name'], o['ordering'], o['target_ordering'], o[
                    'target_name']
                ordering_process_name = f"{process_name}({ordering})"
                ordering_target_name = f"{target_name}({target_ordering})"
                if area_name not in results:
                    results[area_name] = {'work_area': area_name, 'links': [{'source': ordering_process_name,
                                                                             'target': target_name if not target_name else ordering_target_name}]}
                else:
                    results[area_name]['links'].append({'source': ordering_process_name, 'target': ordering_target_name})
                _area_process[area_name] = _area_process.get(area_name, []) + [ordering_process_name]
            # 绘制点的信息
            for k, v in results.items():
                process_list = _area_process[k]
                v['data'] = self.generate_circle_layout(process_list, center_x, center_y, radius)
        except Exception as e:
            e_logger.error(f'生成工序循环图异常, 异常信息: {e}')
            raise ValidationError('生成工序循环图异常！')
        return Response(list(results.values()))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        export = self.request.query_params.get('export')
        all_flag = self.request.query_params.get('all')
        out_rail_flat = self.request.query_params.get('out_rail_flat')
        out_empty_flat = self.request.query_params.get('out_empty_flat')
        if out_rail_flat:  # 只下料的工艺段
            queryset = queryset.filter(Q(upper_rail_type=2) | Q(lower_rail_type=2))
        if out_empty_flat:  # 下空花篮的工艺段
            queryset = queryset.filter(Q(upper_rail_type=2, upper_basket_type__in=(1, 3, 5)) | Q(lower_rail_type=2, lower_basket_type__in=(1, 3, 5)))
        if export:
            data = self.get_serializer(queryset, many=True).data
            return gen_template_response(self.EXPORT_FIELDS_DICT, data, self.FILE_NAME,
                                         self.SHEET_NAME, self.TEMPLATE_FILE)
        if all_flag and self.VALUES_FIELDS:
            return Response(queryset.values(*self.VALUES_FIELDS))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @atomic
    @action(methods=['post'], detail=False, url_path='import_xlsx', url_name='import_xlsx')
    def import_xlsx(self, request):
        file = self.request.FILES.get('file')
        # 读取file 并且存入数据库
        if not file:
            raise ValidationError('请上传文件')
        cur_sheet = get_cur_sheet(file)
        if cur_sheet.ncols < 13:
            raise ValidationError('导入文件数据列数错误！')
        try:
            data = get_sheet_data(cur_sheet, start_row=1)
            rail_type = {'上料': 1, '下料': 2}
            basket_type = {'空叠片盒': 1, '满叠片盒': 2, '空湿花篮': 3, '满湿花篮': 4, '空干花篮': 5, '满干花篮': 6}
            create_data = []
            for item in data:
                process_name = item[0]
                ordering = int(item[1])
                source_process = item[2] if item[2] else None
                target_process = item[3] if item[3] else None
                working_area = item[5].strip() if item[5] else None
                upper_rail_type = item[6].strip() if item[6] else None
                upper_basket_type = item[7].strip() if item[7] else None
                lower_rail_type = item[8].strip() if item[8] else None
                lower_basket_type = item[9].strip() if item[9] else None
                cell_numbers = int(item[10])
                q_time = int(item[11])
                pitch_time = int(item[12])
                if not all([process_name, ordering, working_area, cell_numbers, q_time, pitch_time]):
                    raise ValidationError('校验异常: 工艺段名称、工艺段顺序、车间号、工作区、单车电池片数量、物料超时时间(秒)、节拍(秒)不能为空！')
                working_area_instance = GlobalCode.objects.filter(global_name=working_area).last()
                if not working_area_instance:
                    raise ValidationError('校验异常: 工作区不存在！')
                if source_process and not ProcessSection.objects.filter(source_process__process_name=source_process).exists():
                    raise ValidationError('校验异常: 源工艺段不存在！')
                if target_process and not ProcessSection.objects.filter(target_process__process_name=source_process).exists():
                    raise ValidationError('校验异常: 目标工艺段不存在！')
                if not all([upper_rail_type, lower_rail_type]):
                    raise ValidationError('校验异常: 上下层轨道上下料类型必须填一个！')
                if upper_rail_type and not rail_type.get(upper_rail_type):
                    raise ValidationError('校验异常: 上层轨道上下料类型不存在！')
                if upper_basket_type and not basket_type.get(upper_basket_type):
                    raise ValidationError('校验异常: 上层花篮类型不存在！')
                if lower_rail_type and not rail_type.get(lower_rail_type):
                    raise ValidationError('校验异常: 下层轨道上下料类型不存在！')
                if lower_basket_type and not basket_type.get(lower_basket_type):
                    raise ValidationError('校验异常: 下层花篮类型不存在！')
                create_data.append({
                    'process_name': process_name, 'ordering': ordering, 'source_process': source_process, 'target_process': target_process,
                    'working_area': working_area_instance.id, 'cell_numbers': cell_numbers, 'q_time': q_time,
                    'upper_rail_type': upper_rail_type if not upper_rail_type else rail_type.get(upper_rail_type),
                    'upper_basket_type': upper_basket_type if not upper_basket_type else basket_type.get(upper_basket_type),
                    'lower_rail_type': lower_rail_type if not lower_rail_type else rail_type.get(lower_rail_type),
                    'lower_basket_type': lower_basket_type if not lower_basket_type else basket_type.get(lower_basket_type),
                    'pitch_time': pitch_time,
                })
            s = self.get_serializer(data=create_data, many=True)
            if not s.is_valid(raise_exception=False):
                e_logger.error(f'校验异常: 添加数据出现异常, 检查数据！{s.errors}')
                raise ValidationError(f'校验异常: 添加数据出现异常, 检查数据！')
            s.save()
        except Exception as e:
            err_msg = e.args[0] if '校验异常' in e.args[0] else '导入文件数据时发生错误！'
            e_logger.error(e.args[0])
            raise ValidationError(err_msg)
        return Response('导入成功')


@method_decorator([api_recorder], name="dispatch")  # 本来是删除，现在改为是启用就改为禁用 是禁用就改为启用
class PlatFormInfoViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = PlatFormInfo.objects.select_related('process__working_area', 'group')
    filter_class = PlatFormInfoFilter
    filter_backends = (DjangoFilterBackend, PlatFormInfoOrderingFilter)
    VALUES_FIELDS = ['id', 'platform_ID', 'platform_name', 'process__process_name',
                     'process', 'is_used']
    ordering_fields = ('platform_ID', 'platform_name', 'desc', 'location_name', 'process_name',
                       'upper_rail_type', 'lower_rail_type', 'is_used'
                       'q_time', 'pitch_time', 'location_group_name', 'created_time', 'created_username', 'working_area_name')
    ordering = ['process__ordering', 'platform_ID']
    EXPORT_FIELDS_DICT = {
        '站台ID': 'platform_ID',
        '站台名称': 'platform_name',
        '站台描述': 'desc',
        '位置点名称': 'location_name',
        '工作区': 'working_area_name',
        '所属工艺段': 'process_name',
        '物料超时时间（秒）': 'q_time',
        '节拍（秒）': 'pitch_time',
        'AGV动作1': 'action1',
        'AGV动作2': 'action2',
        'AGV动作3': 'action3',
        'AGV动作4': 'action4',
        '休息位组': 'location_group_name',
        '任务触发方式': 'task_trigger_type_name',
        '上料触发阈值（篮）': 'up_task_trigger_threshold',
        '下料触发阈值（篮）': 'down_task_trigger_threshold',
        '互斥站台': 'rejected_platform_names',
        '是否干式设备': 'is_dry_type_flag',
        '湿区设备限制组': 'wet_limit_group_names',
        '湿式设备组阈值': 'wet_group_threshold',
        '任务延时时间（s）': 'task_delay_time',
        '任务优先级': 'task_priority'
    }
    FILE_NAME = '工艺站台列表.xlsx'

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return PlatFormInfoUpdateSerializer
        elif self.action == 'create':
            return PlatFormInfoCreateSerializer
        return PlatFormInfoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        export = self.request.query_params.get('export')
        all_flag = self.request.query_params.get('all')
        if export:
            data = PlatFormExportSerializer(queryset, many=True).data
            return gen_template_response(self.EXPORT_FIELDS_DICT, data, self.FILE_NAME,
                                         self.SHEET_NAME, self.TEMPLATE_FILE)
        if all_flag and self.VALUES_FIELDS:
            return Response(queryset.values(*self.VALUES_FIELDS))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @atomic()
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated], url_path='batch-update',
            url_name='batch-update')
    def batch_update(self, request):
        """批量启用、停用"""
        obj_ids = self.request.data.get('obj_ids')
        for i in obj_ids:
            try:
                instance = self.get_queryset().get(id=i)
            except Exception:
                raise ValidationError('object does not exists!')
            if instance.is_used:
                instance.is_used = False
                plt_task = Tasks.objects.filter(platform_ID=instance.platform_ID, state__in=(1, 2, 3, 4, 5, 6)).first()
                if plt_task:
                    if plt_task.rcs_order_id:
                        data = [{'order_id': plt_task.rcs_order_id, 'order_command_type_id': 2}]
                        res_data, recode = cancel_task(data)
                        if recode != 200:
                            e_logger.error('禁用站台：{}，任务取消失败'.format(instance.platform_ID))
            else:
                instance.is_used = True
            setattr(instance, 'last_updated_user', self.request.user)
            instance.save()
        return Response('ok')

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], url_path='download-template',
            url_name='download-template')
    def download_template(self, request):
        return FileResponse(open('xlsx_template/工艺站台模板.xlsx', 'rb'))

    @atomic()
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], url_path='import-xlsx',
            url_name='import-xlsx')
    def import_xlx(self, request):
        excel_file = request.FILES.get('file', None)
        if not excel_file:
            raise ValidationError('文件不可为空！')
        cur_sheet = get_cur_sheet(excel_file)
        if cur_sheet.ncols != 22:
            raise ValidationError('导入文件数据错误！')
        data = get_sheet_data(cur_sheet, start_row=1)
        user_list = []
        process_dict = dict(ProcessSection.objects.values_list('process_name', 'id'))
        location_group_dict = dict(LocationGroup.objects.values_list('group_name', 'id'))
        plt_group_dict = dict(PlatformGroup.objects.values_list('group_name', 'id'))
        existed_platform_ID = PlatFormInfo.objects.values_list('platform_ID', flat=True)
        existed_platform_name = PlatFormInfo.objects.values_list('platform_name', flat=True)
        existed_location_name = PlatFormInfo.objects.values_list('location_name', flat=True)
        existed_desc = PlatFormInfo.objects.values_list('desc', flat=True)
        process_data = ProcessSection.objects.values('process_name', 'upper_rail_type', 'lower_rail_type')
        process_data_dict = {i['process_name']: {'upper_rail_type': i['upper_rail_type'],'lower_rail_type': i['lower_rail_type']} for i in process_data}
        for item in data:
            plt_data = {
                "platform_ID": item[0],
                "platform_name": item[1],
                "desc": item[2],
                "location_name": item[3],
                "process": item[5],
                "q_time": item[6],
                "pitch_time": item[7],
                "location_group": item[12],
                "task_trigger_type": item[13],
                "up_task_trigger_threshold": None if item[14] == '' else item[14],
                "down_task_trigger_threshold": None if item[15] == '' else item[15],
                "is_dry_type": None if not item[17] else item[17],
                "wet_limit_groups": item[18],
                "wet_group_threshold": None if not item[19] else item[19],
                "task_delay_time": 0 if not item[20] else item[20],
                "task_priority": 1 if not item[21] else item[21]
            }
            user_list.append(plt_data)
        s = PlatFormImportSerializer(data=user_list, many=True, context={'request': self.request})
        if not s.is_valid():
            for i in s.errors:
                if i:
                    raise ValidationError(list(i.values())[0])
        validated_data = s.validated_data
        platform_ID_list = []
        platform_name_list = []
        desc_list = []
        location_name_list = []
        platform_instance_list = []
        task_trigger_type_dict = {'以上料阈值': 1, '以下料阈值': 2, '关闭': 0}
        for item in validated_data:
            platform_ID = item['platform_ID'].rstrip('.0')
            platform_ID_list.append(platform_ID)
            platform_name_list.append(item['platform_name'])
            desc_list.append(item['desc'])
            loc_name = item['location_name']
            location_name_list.append(loc_name)
            process_name = item['process']
            location_group_name = item['location_group']
            task_trigger_type_name = item['task_trigger_type']
            up_task_trigger_threshold = item['up_task_trigger_threshold']
            down_task_trigger_threshold = item['down_task_trigger_threshold']
            wet_limit_group_names = [] if not item['wet_limit_groups'] else item['wet_limit_groups'].split('/')
            process_id = process_dict.get(process_name)
            location_group_id = location_group_dict.get(location_group_name)
            wet_limit_group_ids = []
            if task_trigger_type_name not in task_trigger_type_dict:
                raise ValidationError('站台:{}，任务触发方式错误！'.format(platform_ID))
            task_trigger_type = task_trigger_type_dict.get(task_trigger_type_name)
            for w in wet_limit_group_names:
                wg = plt_group_dict.get(w)
                if not wg:
                    raise ValidationError('站台:{}，湿区设备限制组【{}】不存在！'.format(platform_ID, wg))
                wet_limit_group_ids.append(wg)
            if (task_trigger_type == 1 and up_task_trigger_threshold in [None, '']) or (task_trigger_type == 2 and down_task_trigger_threshold in [None, '']):
                raise ValidationError('站台:{}，任务上下触发阈值必填！'.format(platform_ID))
            if not process_id:
                raise ValidationError('站台:{}，所属工艺段名称【{}】不存在！'.format(platform_ID, process_name))
            # if not location_group_id:
            #     raise ValidationError('站台:{}，休息位组【{}】不存在！'.format(platform_ID, location_group_name))
            plt_process = process_data_dict[process_name]
            if all([plt_process['upper_rail_type'], plt_process['lower_rail_type']]):
                platform_type = 3
            elif plt_process['upper_rail_type'] or plt_process['lower_rail_type'] == 1:
                platform_type = 1
                task_trigger_type = 1
            elif plt_process['upper_rail_type'] or plt_process['lower_rail_type'] == 2:
                platform_type = 2
                task_trigger_type = 2
            else:
                platform_type = 1
            part_data = {
                1: {'axis_no': 1, 'slot_no': 'G2B', 'part_type': None, 'location_ID': '{}_4'.format(loc_name)},
                2: {'axis_no': 2, 'slot_no': 'G2A', 'part_type': None, 'location_ID': '{}_3'.format(loc_name)},
                3: {'axis_no': 3, 'slot_no': 'G1B', 'part_type': None, 'location_ID': '{}_2'.format(loc_name)},
                4: {'axis_no': 4, 'slot_no': 'G1A', 'part_type': None, 'location_ID': '{}_1'.format(loc_name)},
            }
            if plt_process['upper_rail_type'] == 1:
                part_data[1]['part_type'] = 2
                part_data[2]['part_type'] = 2
            elif plt_process['upper_rail_type'] == 2:
                part_data[1]['part_type'] = 1
                part_data[2]['part_type'] = 1
            if plt_process['lower_rail_type'] == 1:
                part_data[3]['part_type'] = 2
                part_data[4]['part_type'] = 2
            elif plt_process['lower_rail_type'] == 2:
                part_data[3]['part_type'] = 1
                part_data[4]['part_type'] = 1
            is_dry_type_flag = item['is_dry_type']
            if is_dry_type_flag == '是':
                is_dry_type = True
            elif is_dry_type_flag == '否':
                is_dry_type = False
            else:
                is_dry_type = None
            plt_instance_data = {
                "platform_ID": platform_ID,
                "platform_name": item['platform_name'],
                "desc": item['desc'],
                "location_name": item['location_name'],
                "process_id": process_id,
                "q_time": item['q_time'],
                "pitch_time": item['pitch_time'],
                "location_group_id": location_group_id,
                "task_trigger_type": task_trigger_type,
                "up_task_trigger_threshold": up_task_trigger_threshold,
                "down_task_trigger_threshold": down_task_trigger_threshold,
                "is_dry_type": is_dry_type,
                "wet_limit_groups": wet_limit_group_ids if is_dry_type is False else [],
                "wet_group_threshold": item['wet_group_threshold'] if is_dry_type is False else None,
                "task_delay_time": item['task_delay_time'],
                "task_priority": item['task_priority'],
                "platform_type": platform_type,
                "part_data": part_data.values(),
                "created_user": self.request.user
            }
            platform_instance_list.append(plt_instance_data)

        if len(platform_ID_list) != len(set(platform_ID_list)):
            raise ValidationError('导入数据中存在相同的站台ID，请修改后重试！')

        if len(platform_name_list) != len(set(platform_name_list)):
            raise ValidationError('导入数据中存在相同的站台名称，请修改后重试！')

        if len(desc_list) != len(set(desc_list)):
            raise ValidationError('导入数据中存在相同的站台描述，请修改后重试！')

        if len(location_name_list) != len(set(location_name_list)):
            raise ValidationError('导入数据中存在相同的位置点名称，请修改后重试！')

        common_plt_ID = set(existed_platform_ID) & set(platform_ID_list)
        common_plt_name = set(existed_platform_name) & set(platform_name_list)
        common_plt_desc = set(existed_desc) & set(desc_list)
        common_plt_location = set(existed_location_name) & set(location_name_list)

        if common_plt_ID:
            raise ValidationError('以下站台ID已存在，请剔除后重试！：{}'.format('、'.join(common_plt_ID)))

        if common_plt_name:
            raise ValidationError('以下站台名称已存在，请剔除后重试！：{}'.format('、'.join(common_plt_name)))

        if common_plt_desc:
            raise ValidationError('以下站台描述已存在，请剔除后重试！：{}'.format('、'.join(common_plt_desc)))

        if common_plt_location:
            raise ValidationError('以下站台位置点已存在，请剔除后重试！：{}'.format('、'.join(common_plt_location)))

        for instance_data in platform_instance_list:
            wet_limit_groups = instance_data.pop('wet_limit_groups')
            part_data = instance_data.pop('part_data')
            plt_instance = PlatFormInfo.objects.create(**instance_data)
            plt_instance.wet_limit_groups.set(wet_limit_groups)
            PlatFormRealInfo.objects.create(platform_info=plt_instance)
            part_data_list = []
            for pp in part_data:
                pp['platform_info'] = plt_instance
                part_data_list.append(PlatformPart(**pp))
            PlatformPart.objects.bulk_create(part_data_list)
        return Response('ok')


@method_decorator([api_recorder], name="dispatch")  # 本来是删除，现在改为是启用就改为禁用 是禁用就改为启用
class CacheDeviceInfoViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = CacheDeviceInfo.objects.filter(delete_flag=False)
    filter_class = CacheDeviceInfoFilter
    ordering = ['device_ID']
    filter_backends = (DjangoFilterBackend, CacheDeviceInfoOrderingFilter)
    ordering_fields = ('device_ID', 'device_name', 'ordering', 'desc', 'in_location_name',
                       'out_location_name', 'working_area__area_name', 'allow_task_num',
                       'created_time', 'created_username', 'in_is_used', 'out_is_used', 'task_priority')
    VALUES_FIELDS = ['id', 'device_ID', 'device_name', 'desc', 'in_is_used', 'out_is_used']

    def get_serializer_class(self):
        if self.action == 'list':
            return CacheDeviceInfoSerializer
        return CacheDeviceInfoUpdateSerializer

    @atomic()
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated], url_path='batch-update',
            url_name='batch-update')
    def batch_update(self, request):
        """批量启用、停用"""
        obj_ids = self.request.data.get('obj_ids')
        operator_type = self.request.data.get('operator_type')  # 1 进料、2 出料
        if not obj_ids:
            raise ValidationError('未勾选堆栈数据！')
        for i in obj_ids:
            try:
                instance = self.get_queryset().get(id=i)
            except Exception:
                raise ValidationError('object does not exists!')
            if operator_type == 1:
                if instance.in_is_used:
                    instance.in_is_used = False
                else:
                    instance.in_is_used = True
            else:
                if instance.out_is_used:
                    instance.out_is_used = False
                else:
                    instance.out_is_used = True
            setattr(instance, 'last_updated_user', self.request.user)
            instance.save()
        return Response('ok')

    @atomic()
    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated], url_path='batch-destroy',
            url_name='batch-destroy')
    def batch_destroy(self, request):
        obj_ids = self.request.data.get('obj_ids')
        try:
            qs = self.get_queryset().filter(id__in=obj_ids)
            device_names = list(qs.values_list('device_name', flat=True))
            self.get_queryset().filter(id__in=obj_ids).delete()
        except ProtectedError:
            raise ValidationError('非法操作，请删除相关联数据后再试！')
        CacheDeviceStock.objects.filter(equip_code__in=device_names).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 已弃用
@method_decorator([api_recorder], name="dispatch")  # 本来是删除，现在改为是启用就改为禁用 是禁用就改为启用
class RestLocationViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = RestLocation.objects.filter(delete_flag=False).order_by("location_name")
    serializer_class = RestLocationSerializer
    # permission_classes = (IsAuthenticated,)
    filter_class = RestLocationFilter
    filter_backends = (DjangoFilterBackend, RestLocationOrderingFilter)
    ordering_fields = ('location_ID', 'location_code', 'location_name', 'desc',
                       'working_area', 'is_used', 'created_time', 'created_username')
    ordering = ('location_ID',)
    VALUES_FIELDS = ['id', 'location_ID', 'location_code', 'location_name', 'working_area', 'is_used']


@method_decorator([api_recorder], name="dispatch")  # 本来是删除，现在改为是启用就改为禁用 是禁用就改为启用
class LocationViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = LocationFilter
    filter_backends = (DjangoFilterBackend, LocationOrderingFilter)
    ordering_fields = ('location_name', 'is_used', 'created_username', 'created_time', 'last_updated_time', 'last_updated_username')
    ordering = ('location_name',)
    VALUES_FIELDS = ['id', 'location_name', 'is_used']

    @action(methods=['post'], detail=False, url_path='sync-location', url_name='sync-location')
    def sync_location(self, request):
        """同步休息位"""
        data, code = get_rest_locations()
        if code == 200 and "code" in data and data["code"] == 0:
            success_list = data["data"]['data']
            existed_locations = Location.objects.values_list('location_name', flat=True)
            diff_locations = set(success_list) - set(existed_locations)
            lc_list = []
            for item in diff_locations:
                lc_data = {'location_name': item, 'created_user': self.request.user}
                lc_list.append(Location(**lc_data))
            if lc_list:
                Location.objects.bulk_create(lc_list)
            return Response('同步休息位成功！')
        else:
            raise ValidationError('同步休息位失败，请联系管理员！')


@method_decorator([api_recorder], name="dispatch")  # 本来是删除，现在改为是启用就改为禁用 是禁用就改为启用
class LocationGroupViewSet(CommonExportListMixin, CommonBatchDestroyView, ModelViewSet):
    queryset = LocationGroup.objects.all()
    serializer_class = LocationGroupSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = LocationGroupFilter
    filter_backends = (DjangoFilterBackend, LocationOrderingFilter)
    ordering_fields = ('group_code', 'group_name', 'created_username', 'created_time', 'last_updated_time', 'last_updated_username')
    ordering = ('group_code',)
    VALUES_FIELDS = ['id', 'group_code', 'group_name']


@method_decorator([api_recorder], name="dispatch")
class RoutingSchemaViewSet(ModelViewSet):
    queryset = RoutingSchema.objects.order_by('id')
    serializer_class = RoutingSchemaSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return RoutingSchemaUpdateSerializer
        return RoutingSchemaSerializer

    @action(methods=['get'], detail=False, url_path='current-route', url_name='current-route')
    def current_route(self, request):
        """当前定线（所有已启用的定线）"""
        all_route = self.request.query_params.get('all_route')
        processes = ProcessSection.objects.order_by('ordering').values('id', 'process_name')
        queryset_data = RoutingSchema.objects.filter(is_used=True).order_by('id').values('id', 'route_ID', 'route_name')
        if all_route:
            return Response(queryset_data.values_list('route_name', flat=True).order_by('id'))
        ret = []

        # 已定线机台/堆栈
        for queryset in queryset_data:
            process_plats_data = {
                i['id']: {
                    "process_name": i['process_name'],
                    "process_id": i['id'],
                    "plt_devices": []}
                for i in processes
            }
            # 已定线机台
            plt_rlt = PlatFormInfo.objects.filter(
                group__route_schema=queryset['id']).values(
                'id', 'desc',
                'process_id').order_by('desc')
            # 已定线堆栈
            cache_rlt = CacheDeviceRouteRelation.objects.filter(
                group__route_schema=queryset['id']).values(
                'cache_device_id', 'cache_device__desc',
                'group__process_id').order_by('cache_device__desc')
            for item1 in plt_rlt:
                process_id = item1['process_id']
                platform_id = item1['id']
                platform_desc = item1['desc']
                process_plats_data[process_id]['plt_devices'].append(
                    {"instance_id": platform_id, "instance_name": platform_desc, "dp_type": 1}
                )
            for item2 in cache_rlt:
                process_id = item2['group__process_id']
                device_id = item2['cache_device_id']
                device_desc = item2['cache_device__desc']
                process_plats_data[process_id]['plt_devices'].append(
                    {"instance_id": device_id, "instance_name": device_desc, "dp_type": 2}
                )
            ret.append(
                {"id": queryset['id'],
                 "route_name": queryset['route_name'],
                 "route_ID": queryset['route_ID'],
                 "process_plats": process_plats_data.values()
                 }
            )

        return Response(ret)

    def list(self, request, *args, **kwargs):
        """预定线（所有定线，包括已启用、已禁用、暂存）"""
        processes = ProcessSection.objects.order_by('ordering').values('id', 'process_name')
        queryset_data = RoutingSchema.objects.order_by('id').values('id', 'route_ID', 'route_name', 'is_used', 'stash_flag', 'is_forbidden')
        ret = []
        all_platform = PlatFormInfo.objects.values(instance_id=F('id'), instance_name=F('desc'), pc_id=F('process_id'), dp_type=Value(1, output_field=IntegerField())).order_by('instance_name')
        all_device = ProcessCacheDeviceRelation.objects.values(instance_id=F('cache_device_id'), instance_name=F('cache_device__desc'), pc_id=F('process_id'), dp_type=Value(2, output_field=IntegerField())).order_by('instance_name')

        routing_plt_ids = []
        routing_cache_ids = []
        # 已定线机台/堆栈
        for queryset in queryset_data:
            is_used = queryset['is_used']
            is_forbidden = queryset['is_forbidden']
            stash_flag = queryset['stash_flag']
            process_plats_data = {
                i['id']: {
                    "process_name": i['process_name'],
                    "process_id": i['id'],
                    "plt_devices": []}
                for i in processes
            }
            if not stash_flag:
                # 启用、禁用状态下已定线机台
                plt_rlt = PlatFormInfo.objects.filter(
                    group__route_schema=queryset['id']).values(
                    'id', 'desc', 'process_id', 'group_id').order_by('desc')
                # 启用、禁用状态下已定线堆栈
                cache_rlt = CacheDeviceRouteRelation.objects.filter(
                    group__route_schema=queryset['id']).values(
                    'cache_device_id', 'cache_device__desc',
                    'group__process_id', 'group_id').order_by('cache_device__desc')
            else:
                # 暂存状态下已定线机台
                plt_rlt = PlatFormInfo.objects.filter(
                    pre_group__route_schema=queryset['id']).values(
                    'id', 'desc', 'process_id', 'pre_group_id').order_by('desc')
                # 暂存状态下已定线堆栈
                cache_rlt = CacheDevicePreRouteRelation.objects.filter(
                    group__route_schema=queryset['id']).values(
                    'cache_device_id', 'cache_device__desc',
                    'group__process_id', 'group_id').order_by('cache_device__desc')
            for item1 in plt_rlt:
                process_id = item1['process_id']
                platform_id = item1['id']
                platform_desc = item1['desc']
                if not stash_flag:
                    group_id = item1['group_id']
                else:
                    group_id = item1['pre_group_id']
                routing_plt_ids.append(platform_id)
                process_plats_data[process_id]['plt_devices'].append(
                    {"instance_id": platform_id, "instance_name": platform_desc, "dp_type": 1, 'group_id': group_id, 'pc_id': process_id}
                )
            for item2 in cache_rlt:
                process_id = item2['group__process_id']
                device_id = item2['cache_device_id']
                device_desc = item2['cache_device__desc']
                group_id = item2['group_id']
                routing_cache_ids.append(device_id)
                process_plats_data[process_id]['plt_devices'].append(
                    {"instance_id": device_id, "instance_name": device_desc, "dp_type": 2, 'group_id': group_id, 'pc_id': process_id}
                )
            ret.append(
                {"id": queryset['id'],
                 "route_name": queryset['route_name'],
                 "route_ID": queryset['route_ID'],
                 'stash_flag': stash_flag,
                 'is_used': is_used,
                 'is_forbidden': is_forbidden,
                 "process_plats": process_plats_data.values()
                 }
            )
        # 未定线机台/堆栈
        un_routing_line_data = {"id": None, "route_name": "未定线", "process_plats": []}
        for p in processes:
            un_routing_plt = filter(lambda x: x['pc_id'] == p['id'] and x['instance_id'] not in routing_plt_ids, all_platform)
            un_routing_device = filter(lambda x: x['pc_id'] == p['id'], all_device)

            un_routing_line_data['process_plats'].append(
                {
                    "process_name": p['process_name'],
                    "process_id": p['id'],
                    "plt_devices": list(un_routing_plt) + list(un_routing_device)
                }
            )
        ret.append(un_routing_line_data)
        return Response(ret)


@method_decorator([api_recorder], name="dispatch")
class PlatformGroupViewSet(CommonExportListMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           GenericViewSet):
    queryset = PlatformGroup.objects.all()
    serializer_class = PlatformGroupSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = PlatformGroupFilter
    VALUES_FIELDS = ['id', 'group_name', 'group_ID']
    ordering = ('route_schema_id', 'group_ID')
    ordering_fields = ['group_ID', 'group_name', 'maximum', 'minimum', 'warning_maximum', 'warning_minimum']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        export = self.request.query_params.get('export')
        all_flag = self.request.query_params.get('all')
        out_rail_flat = self.request.query_params.get('out_rail_flat')
        fl_flag = self.request.query_params.get('fl_flag')
        if out_rail_flat:
            queryset = queryset.filter(Q(process__upper_rail_type=2) | Q(process__lower_rail_type=2))
        if fl_flag:
            pg_ids = set(PlatformGroup.objects.filter(shunt_plts__isnull=False).values_list('id', flat=True))
            queryset = queryset.filter(id__in=pg_ids)
        if export:
            data = self.get_serializer(queryset, many=True).data
            return gen_template_response(self.EXPORT_FIELDS_DICT, data, self.FILE_NAME,
                                         self.SHEET_NAME, self.TEMPLATE_FILE)
        if all_flag and self.VALUES_FIELDS:
            return Response(queryset.values(*self.VALUES_FIELDS))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@method_decorator([api_recorder], name="dispatch")
class EmptyBasketRouteSchemaView(APIView):

    def get(self, request):
        process_id = self.request.query_params.get('process_id')
        if not process_id:
            return Response([])
        try:
            process = ProcessSection.objects.get(id=process_id)
        except Exception:
            raise ValidationError('参数错误')
        if not ((process.upper_rail_type == 2 and process.upper_basket_type in (1, 3, 5)) or
                (process.lower_rail_type == 2 and process.lower_basket_type in (1, 3, 5))):
            return Response([])
        if process.upper_rail_type == 2:
            up_basket_type = process.get_upper_basket_type_display()
        else:
            up_basket_type = process.get_lower_basket_type_display()
        # 该工序所有出空花篮设备
        output_plts = PlatFormInfo.objects.filter(process_id=process_id).order_by('platform_ID')
        output_caches = ProcessCacheDeviceRelation.objects.filter(process_id=process_id).order_by('cache_device__device_ID')
        # 所有进空花篮设备
        all_routing_plts = list(PlatFormInfo.objects.filter(
            process=process.target_process).values(instance_id=F('id'), name=F('desc')).order_by('instance_id'))
        ret = []
        for output_plt in output_plts:
            if hasattr(output_plt, 'p_route'):
                route_plts = output_plt.p_route.target_platforms.values_list('id', flat=True)
            else:
                route_plts = []
            ret.append({
                'dp_type': 1,
                'instance_id': output_plt.id,
                'instance_name': output_plt.desc,
                'up_basket_type': up_basket_type,
                'routing_plats': route_plts,
            })
        for output_cache in output_caches:
            if hasattr(output_cache.cache_device, 'c_route'):
                route_plts = output_cache.cache_device.c_route.target_platforms.filter(process=process.target_process).values_list('id', flat=True)
            else:
                route_plts = []
            ret.append({
                'dp_type': 2,
                'instance_id': output_cache.cache_device_id,
                'instance_name': output_cache.cache_device.desc,
                'up_basket_type': up_basket_type,
                'routing_plats': route_plts,
            })
        return Response({'data': ret, 'all_routing_plts': all_routing_plts})

    @atomic()
    def post(self, request):
        if not isinstance(self.request.data, dict):
            raise ValidationError('参数错误！')
        data = self.request.data.get('plt_date')
        process_id = self.request.data.get('process_id')
        for item in data:
            dp_type = item['dp_type']
            instance_id = item['instance_id']
            routing_plats = item['routing_plats']
            if dp_type == 1:
                try:
                    plt = PlatFormInfo.objects.get(id=instance_id)
                except Exception:
                    raise ValidationError('该站台不存在！')
                instance = EmptyBasketRouteSchema.objects.filter(platform_info=plt).first()
                if not instance:
                    instance = EmptyBasketRouteSchema.objects.create(
                        route_ID=plt.platform_ID,
                        route_name=plt.desc,
                        platform_info=plt)
                    instance.target_platforms.set(PlatFormInfo.objects.filter(id__in=routing_plats))
                else:
                    instance.target_platforms.clear()
                    instance.target_platforms.set(PlatFormInfo.objects.filter(id__in=routing_plats))
            else:
                try:
                    cache = CacheDeviceInfo.objects.get(id=instance_id)
                except Exception:
                    raise ValidationError('该堆栈不存在！')
                instance = EmptyCacheRouteSchema.objects.filter(cache_info=cache).first()
                if not instance:
                    instance = EmptyCacheRouteSchema.objects.create(
                        route_ID=cache.device_ID,
                        route_name=cache.desc,
                        cache_info=cache)
                    instance.target_platforms.set(PlatFormInfo.objects.filter(id__in=routing_plats))
                else:
                    instance.target_platforms.clear()
                    instance.target_platforms.set(PlatFormInfo.objects.filter(id__in=routing_plats))
        return Response('OK')


@method_decorator([api_recorder], name="dispatch")
class EquipLocationView(APIView):

    def get(self, request):
        pl = list(PlatFormInfo.objects.filter(
            location_name__isnull=False).order_by('process__ordering', 'platform_ID').values('platform_name', 'location_name'))
        cl = CacheDeviceInfo.objects.values('device_name', 'in_location_name', 'out_location_name').order_by('device_name')
        for i in cl:
            device_name = i['device_name']
            in_location = i['in_location_name']
            out_location = i['out_location_name']
            pl.append({'platform_name': '{}进料口'.format(device_name), 'location_name': in_location})
            pl.append({'platform_name': '{}出料口'.format(device_name), 'location_name': out_location})
        return Response(pl)


@method_decorator([api_recorder], name="dispatch")
class GlobalSettingsView(APIView):

    def get(self, request):
        # 筛选
        params = self.request.query_params
        q_desc = params.get('desc')
        q_value = params.get('value')
        filter_kwargs = {}
        if q_desc:
            filter_kwargs['desc__icontains'] = q_desc
        if q_value:
            filter_kwargs['value__icontains'] = q_value
        gc = Configuration.objects.filter(**filter_kwargs).order_by('id').values()
        data = []
        for item in gc:
            data.append({
                "type": item['value_type'],
                "desc": item['desc'],
                "value": item['value'],
                "key_name": item['key'],
                "choices": item['choices']
            })
        return Response(data)

    @atomic()
    def post(self, request):
        data = self.request.data
        Configuration.objects.filter(key=data['key_name']).update(value=str(data['value']).strip())
        return Response('写入全局配置成功！')


@method_decorator([api_recorder], name="dispatch")
class ThresholdDisplayViewSet(CommonExportListMixin, ModelViewSet):
    queryset = PlatFormInfo.objects.all()
    serializer_class = ThresholdDisplaySerializer
    # permission_classes = (IsAuthenticated,)
    filter_class = ThresholdDisplayFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('platform_ID', 'platform_name', 'group_id', 'shunt_platform_group_id')
    ordering = ('platform_ID',)


@method_decorator([api_recorder], name="dispatch")
class CheckConfView(APIView):

    def get(self, request):
        ret = []
        plts = PlatFormInfo.objects.filter(Q(location_name__isnull=True) |
                                           Q(task_trigger_type__isnull=True) |
                                           Q(location_group__isnull=True)).order_by('process__ordering', 'platform_ID')
        for plt in plts:
            msg = "站台【{}】：".format(plt.platform_name)
            if not plt.location_name:
                msg += '未配置Xpress点位；'
            if not plt.task_trigger_type:
                msg += '未配置任务触发方式；'
            if not plt.location_group:
                msg += '未配置休息位组；'
            ret.append(msg)
        return Response(ret)


@method_decorator([api_recorder], name="dispatch")
class CurrentSchedulerSearch(APIView):

    def get(self, request):
        date_now = datetime.datetime.now()
        # date_now = datetime.datetime.strptime('2023-10-20 22:12:12', "%Y-%m-%d %H:%M:%S")
        previous_day = datetime.datetime.now() - datetime.timedelta(days=1)
        next_day = datetime.datetime.now() + datetime.timedelta(days=1)

        st = date_now.strftime('%Y-%m-%d 00:00:00')
        et = date_now.strftime('%Y-%m-%d 23:59:59')
        try:
            time_data = json.loads(Configuration.objects.get(key='shift_time').value)
            for shift, shift_time in time_data.items():
                start_time, end_time = shift_time.split("-")
                if shift == '晚班':
                    cp_st = datetime.datetime.strptime(date_now.strftime('%Y-%m-%d') + ' ' + start_time, '%Y-%m-%d %H:%M:%S')
                    cp_et = datetime.datetime.strptime(next_day.strftime('%Y-%m-%d') + ' ' + end_time, '%Y-%m-%d %H:%M:%S')
                else:
                    cp_st = datetime.datetime.strptime(date_now.strftime('%Y-%m-%d') + ' ' + start_time, '%Y-%m-%d %H:%M:%S')
                    cp_et = datetime.datetime.strptime(date_now.strftime('%Y-%m-%d') + ' ' + end_time, '%Y-%m-%d %H:%M:%S')

                if cp_st <= date_now <= cp_et:
                    if shift == "晚班":
                        st = date_now.strftime('%Y-%m-%d') + ' ' + time_data["早班"].split("-")[0]
                        et = date_now.strftime('%Y-%m-%d') + ' ' + time_data["早班"].split("-")[1]
                    else:
                        st = previous_day.strftime('%Y-%m-%d') + ' ' + time_data["晚班"].split("-")[0]
                        et = date_now.strftime('%Y-%m-%d') + ' ' + time_data["晚班"].split("-")[1]
                    break
        except Exception:
            pass
        return Response({'st': st, 'et': et})