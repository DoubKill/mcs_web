import datetime

from django.contrib.auth.models import AnonymousUser
from django.db.models import F, Q
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from agv.models import CacheDeviceStock
from mcs.settings import COMMON_READ_ONLY_FIELDS
from basics.models import GlobalCodeType, GlobalCode, RoutingSchema, PlatformGroup, PlatFormInfo, \
    CacheDeviceRouteRelation, RestLocationRouteRelation, RestLocation, PlatformPart, \
    ProcessSection, CacheDeviceInfo, CacheDevicePart, PlatFormRealInfo, WorkArea, ProcessRestLocationRelation, \
    CacheDevicePreRouteRelation, EmptyBasketRouteSchema, Location, LocationGroup, LocationGroupRelation, \
    EmptyCacheRouteSchema, AgvType


class BaseModelSerializer(serializers.ModelSerializer):
    """封装字段值国际化功能后的模型类序列化器，需要用ModelSerializer请直接继承该类"""
    created_username = serializers.CharField(source='created_user.username', read_only=True, default='')
    last_update_username = serializers.CharField(source='last_updated_user.username', read_only=True, default='')

    def create(self, validated_data):
        """
        可供所有继承该序列化器的子类自动补充created_user
        :param validated_data:
        :return:
        """
        if self.Meta.model.__name__ in ["Permission", "Group"]:
            return super().create(validated_data)
        user = self.context["request"].user
        if isinstance(user, AnonymousUser):
            user = None
        validated_data.update(created_user=user)
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        """
        可供所有继承该序列化器的子类自动补充updated_user
        :param instance:
        :param validated_data:
        :return:
        """
        if self.Meta.model.__name__ in ["Permission", "Group"]:
            return super().update(instance, validated_data)
        user = self.context["request"].user
        if isinstance(user, AnonymousUser):
            user = None
        validated_data.update(last_updated_user=user)
        return super().update(instance, validated_data)


class AgvTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgvType
        fields = '__all__'


class GlobalCodeTypeSerializer(BaseModelSerializer):
    """公共代码类型序列化器"""
    type_name = serializers.CharField(max_length=64,
                                      validators=[
                                          UniqueValidator(queryset=GlobalCodeType.objects.all(),
                                                          message='该代码类型名称已存在'),
                                      ])
    type_no = serializers.CharField(max_length=64,
                                    validators=[
                                        UniqueValidator(queryset=GlobalCodeType.objects.all(),
                                                        message='该代码类型编号已存在'),
                                    ])

    class Meta:
        model = GlobalCodeType
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class GlobalCodeSerializer(BaseModelSerializer):
    """公共代码序列化器"""
    global_no = serializers.CharField(max_length=64, validators=[UniqueValidator(
        queryset=GlobalCode.objects.all(), message='该公共代码编号已存在')])

    class Meta:
        model = GlobalCode
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('global_type', 'global_name'),
                message="该公共代码已存在，请勿重复添加！"
            )
        ]


class WorkAreaSerializer(BaseModelSerializer):
    agv_type_name = serializers.ReadOnlyField(source='agv_type.type_name', default=None)

    class Meta:
        model = WorkArea
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class ProcessSectionSerializer(BaseModelSerializer):
    process_name = serializers.CharField(max_length=128,
                                         validators=[UniqueValidator(queryset=ProcessSection.objects.filter(delete_flag=False), message='该工艺段名称已存在')])
    process_ID = serializers.CharField(max_length=128,
                                         validators=[
                                             UniqueValidator(queryset=ProcessSection.objects.filter(delete_flag=False),
                                                             message='该工艺段ID已存在')])
    ordering = serializers.IntegerField(validators=[UniqueValidator(queryset=ProcessSection.objects.filter(delete_flag=False), message='该顺序已存在')])
    source_process_name = serializers.CharField(source='source_process.process_name', read_only=True, default=None)
    target_process_name = serializers.CharField(source='target_process.process_name', read_only=True, default=None)
    working_area_name = serializers.CharField(source='working_area.area_name', read_only=True, default=None)
    upper_rail_type_name = serializers.CharField(source='get_upper_rail_type_display', read_only=True, default=None)
    upper_basket_type_name = serializers.CharField(source='get_upper_basket_type_display', read_only=True, default=None)
    lower_rail_type_name = serializers.CharField(source='get_lower_rail_type_display', read_only=True, default=None)
    lower_basket_type_name = serializers.CharField(source='get_lower_basket_type_display', read_only=True, default=None)

    def update(self, instance, validated_data):
        if 'q_time' in validated_data:
            PlatFormInfo.objects.filter(process=instance).update(q_time=validated_data['q_time'])
        if 'pitch_time' in validated_data:
            PlatFormInfo.objects.filter(process=instance).update(pitch_time=validated_data['pitch_time'])
        return super().update(instance, validated_data)

    class Meta:
        model = ProcessSection
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class PlatformPartSerializer(serializers.ModelSerializer):
    part_type_name = serializers.ReadOnlyField(source='get_part_type_display', default=None)

    class Meta:
        model = PlatformPart
        fields = ('axis_no', 'slot_no', 'part_type', 'location_ID', 'part_type_name')
        read_only_fields = COMMON_READ_ONLY_FIELDS


class PlatFormInfoUpdateSerializer(BaseModelSerializer):
    platform_parts = PlatformPartSerializer(many=True, help_text="""
    [{"axis_no": "轴号", "slot_no": "轨道号", "part_type": "部件类型 1/2", "location_ID": "locationName"}]""", read_only=True)
    shunt_platform_group_name = serializers.ReadOnlyField(source='shunt_platform_group.group_name', default=None)
    rejected_platform_name = serializers.ReadOnlyField(source='rejected_platform.platform_name', default=None)
    group_name = serializers.ReadOnlyField(source='group.group_name', default=None)
    route_name = serializers.ReadOnlyField(source='group.route_schema.route_name', default=None)
    upper_rail_type = serializers.ReadOnlyField(source='process.upper_rail_type', default=None)
    lower_rail_type = serializers.ReadOnlyField(source='process.lower_rail_type', default=None)
    upper_basket_type = serializers.ReadOnlyField(source='process.upper_basket_type', default=None)
    lower_basket_type = serializers.ReadOnlyField(source='process.lower_basket_type', default=None)
    source_plt_group_name = serializers.ReadOnlyField()
    source_cache_group_name = serializers.ReadOnlyField()
    target_plt_group_name = serializers.ReadOnlyField()
    target_cache_group_name = serializers.ReadOnlyField()
    target_process = serializers.ReadOnlyField(source='process.target_process_id', default=None)
    source_process = serializers.ReadOnlyField(source='process.source_process_id', default=None)
    working_area = serializers.ReadOnlyField(source='process.working_area_id')
    location_name = serializers.CharField(max_length=256, validators=[
        UniqueValidator(queryset=PlatFormInfo.objects.all(), message='位置点已经被使用')])

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        platform_parts = ret['platform_parts']
        sorted_platform_parts = sorted(platform_parts, key=lambda x: x['axis_no'])
        ret['platform_parts'] = sorted_platform_parts
        return ret

    @atomic()
    def update(self, instance, validated_data):
        if 'process' in validated_data:
            if validated_data['process'].id != instance.process_id:  # 工艺段修改后，去除当前站台相关定线信息
                validated_data['group_id'] = None  # 清除设备组
                validated_data['pre_group_id'] = None  # 清除预定线设备组
                validated_data['shunt_platform_group'] = []   # 清除分流设备组
                validated_data['shunt_threshold'] = None  # 清除分流阈值
                EmptyBasketRouteSchema.objects.filter(platform_info=instance).delete()  # 清除空花篮定线
                for ep in instance.p_etrs.all():
                    ep.target_platforms.remove(instance.id)
                for ec in instance.p_cetrs.all():
                    ec.target_platforms.remove(instance.id)
        instance = super().update(instance, validated_data)
        instance.platform_parts.all().delete()
        part_data = {
            1: {'axis_no': 1, 'slot_no': 'G2B', 'part_type': None,
                'location_ID': '{}_4'.format(instance.location_name)},
            2: {'axis_no': 2, 'slot_no': 'G2A', 'part_type': None,
                'location_ID': '{}_3'.format(instance.location_name)},
            3: {'axis_no': 3, 'slot_no': 'G1B', 'part_type': None,
                'location_ID': '{}_2'.format(instance.location_name)},
            4: {'axis_no': 4, 'slot_no': 'G1A', 'part_type': None,
                'location_ID': '{}_1'.format(instance.location_name)},
        }
        if validated_data['process'].upper_rail_type == 1:
            part_data[1]['part_type'] = 2
            part_data[2]['part_type'] = 2
        elif validated_data['process'].upper_rail_type == 2:
            part_data[1]['part_type'] = 1
            part_data[2]['part_type'] = 1
        if validated_data['process'].lower_rail_type == 1:
            part_data[3]['part_type'] = 2
            part_data[4]['part_type'] = 2
        elif validated_data['process'].lower_rail_type == 2:
            part_data[3]['part_type'] = 1
            part_data[4]['part_type'] = 1
        part_data_list = []
        for pp in part_data.values():
            pp['platform_info'] = instance
            part_data_list.append(PlatformPart(**pp))
        PlatformPart.objects.bulk_create(part_data_list)
        return instance

    class Meta:
        model = PlatFormInfo
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS
        extra_kwargs = {'group': {'read_only': True}, 'pre_group': {'read_only': True}}


class PlatFormInfoCreateSerializer(BaseModelSerializer):
    platform_ID = serializers.CharField(max_length=256, validators=[
        UniqueValidator(queryset=PlatFormInfo.objects.all(), message='站台ID已存在')])
    platform_name = serializers.CharField(max_length=256, validators=[
        UniqueValidator(queryset=PlatFormInfo.objects.all(), message='站台名称已存在')])
    location_name = serializers.CharField(max_length=256, validators=[
        UniqueValidator(queryset=PlatFormInfo.objects.all(), message='位置点已经被使用')], required=False)
    # platform_parts = PlatformPartSerializer(many=True, help_text="""
    #     [{"axis_no": "轴号", "slot_no": "轨道号", "part_type": "部件类型 1/2", "location_ID": "locationName"}]""",
    #                                         required=False)

    @atomic()
    def create(self, validated_data):
        instance = super().create(validated_data)
        part_data = {
            1: {'axis_no': 1, 'slot_no': 'G2B', 'part_type': None, 'location_ID': '{}_4'.format(instance.location_name)},
            2: {'axis_no': 2, 'slot_no': 'G2A', 'part_type': None, 'location_ID': '{}_3'.format(instance.location_name)},
            3: {'axis_no': 3, 'slot_no': 'G1B', 'part_type': None, 'location_ID': '{}_2'.format(instance.location_name)},
            4: {'axis_no': 4, 'slot_no': 'G1A', 'part_type': None, 'location_ID': '{}_1'.format(instance.location_name)},
        }
        if instance.process.upper_rail_type == 1:
            part_data[1]['part_type'] = 2
            part_data[2]['part_type'] = 2
        elif instance.process.upper_rail_type == 2:
            part_data[1]['part_type'] = 1
            part_data[2]['part_type'] = 1
        if instance.process.lower_rail_type == 1:
            part_data[3]['part_type'] = 2
            part_data[4]['part_type'] = 2
        elif instance.process.lower_rail_type == 2:
            part_data[3]['part_type'] = 1
            part_data[4]['part_type'] = 1
        part_data_list = []
        for pp in part_data.values():
            pp['platform_info'] = instance
            part_data_list.append(PlatformPart(**pp))
        PlatformPart.objects.bulk_create(part_data_list)
        PlatFormRealInfo.objects.create(platform_info=instance)
        return instance

    class Meta:
        model = PlatFormInfo
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS
        extra_kwargs = {'group': {'read_only': True}, 'pre_group': {'read_only': True}}


class PlatFormInfoSerializer(BaseModelSerializer):
    process_name = serializers.ReadOnlyField(source='process.process_name')
    working_area_name = serializers.ReadOnlyField(source='process.working_area.area_name', default=None)
    upper_rail_type_name = serializers.ReadOnlyField(source='process.get_upper_rail_type_display', default=None)
    upper_basket_type_name = serializers.ReadOnlyField(source='process.get_upper_basket_type_display', default=None)
    lower_rail_type_name = serializers.ReadOnlyField(source='process.get_lower_rail_type_display', default=None)
    lower_basket_type_name = serializers.ReadOnlyField(source='process.get_lower_basket_type_display', default=None)
    upper_rail_type = serializers.ReadOnlyField(source='process.upper_rail_type', default=None)
    upper_basket_type = serializers.ReadOnlyField(source='process.upper_basket_type', default=None)
    lower_rail_type = serializers.ReadOnlyField(source='process.lower_rail_type', default=None)
    lower_basket_type = serializers.ReadOnlyField(source='process.lower_basket_type', default=None)
    location_group_name = serializers.ReadOnlyField(source='location_group.group_name', default=None)

    class Meta:
        model = PlatFormInfo
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class RestLocationSerializer(BaseModelSerializer):
    location_code = serializers.CharField(max_length=256, validators=[UniqueValidator(queryset=RestLocation.objects.all(), message='编号已存在')])
    location_name = serializers.CharField(max_length=256, validators=[UniqueValidator(queryset=RestLocation.objects.all(), message='名称已存在')])
    select_process = serializers.ListField(write_only=True, required=False)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        select_process, select_process_name = [], ''
        processes = instance.processrestlocationrelation_set.all().order_by('process_id')
        for p in processes:
            select_process.append(p.process_id)
            select_process_name += f"{p.process.process_name}" if not select_process_name else f", {p.process.process_name}"
        # 所属定线
        routes = RestLocationRouteRelation.objects.filter(rest_location=instance).values_list('group__route_schema__route_name', flat=True).order_by('group__route_schema__route_ID')
        route_str = ''.join(routes)
        res.update({'select_process': select_process, 'working_area_name': instance.working_area.area_name, 'select_process_name': select_process_name,
                    'route_str': route_str})
        return res

    @atomic
    def create(self, validated_data):
        select_process = validated_data.pop('select_process', [])
        instance = super().create(validated_data)
        for i in select_process:
            ProcessRestLocationRelation.objects.create(rest_location=instance, process_id=i)
        return instance

    @atomic
    def update(self, instance, validated_data):
        select_process = validated_data.pop('select_process', [])
        instance.processrestlocationrelation_set.all().delete()
        for i in select_process:
            ProcessRestLocationRelation.objects.create(rest_location=instance, process_id=i)
        return super().update(instance, validated_data)

    class Meta:
        model = RestLocation
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class RoutingSchemaSerializer(serializers.ModelSerializer):
    process_plats = serializers.ListField(write_only=True)
    route_ID = serializers.CharField(max_length=256,
                                         validators=[
                                             UniqueValidator(queryset=RoutingSchema.objects.all(),
                                                             message='该定线ID已存在！')])
    route_name = serializers.CharField(max_length=256,
                                         validators=[
                                             UniqueValidator(queryset=RoutingSchema.objects.all(),
                                                             message='该定线名称已存在！')])

    @atomic()
    def create(self, validated_data):
        """新建定线（暂存状态）"""
        # validated_data['route_ID'] = '1{}'.format(datetime.datetime.now().strftime("%d%H%M%S"))
        process_plats = validated_data.pop('process_plats', [])
        instance = super().create(validated_data)
        for item in process_plats:
            process_id = item['process_id']
            process = ProcessSection.objects.get(id=process_id)
            process_name = item['process_name']
            plt_devices = item['plt_devices']
            routing_plt = list(filter(lambda x: x['dp_type'] == 1, plt_devices))  # 定线机台
            routing_device = list(filter(lambda x: x['dp_type'] == 2, plt_devices))  # 定线堆栈
            if routing_plt:
                pg = PlatformGroup.objects.create(
                    route_schema=instance,
                    group_ID='{}{}{}'.format('1', process.process_ID, instance.route_ID),
                    group_name='{}-{}-{}'.format(instance.route_name, process_name, 'AUTO'),
                    process_id=process_id,
                    group_type=1
                )
                PlatFormInfo.objects.filter(id__in=[i['instance_id'] for i in routing_plt]).update(pre_group_id=pg)
            if routing_device:
                pg = PlatformGroup.objects.create(
                    route_schema=instance,
                    group_ID='{}{}{}'.format('2', process.process_ID, instance.route_ID),
                    group_name='{}-{}-{}'.format(instance.route_name, process_name, 'BUFFER'),
                    process_id=process_id,
                    group_type=2
                )
                for dv in routing_device:
                    CacheDevicePreRouteRelation.objects.create(
                        cache_device_id=dv['instance_id'],
                        group=pg
                    )
        return instance

    class Meta:
        model = RoutingSchema
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class RoutingSchemaUpdateSerializer(serializers.ModelSerializer):
    process_plats = serializers.ListField(write_only=True)
    operation_type = serializers.IntegerField(write_only=True)

    @atomic()
    def update(self, instance, validated_data):
        operation_type = validated_data['operation_type']
        if operation_type == 3:  # 禁用(只有启用后才可禁用)
            if not instance.is_used:
                raise serializers.ValidationError('操作失败，当前定线未启用！')
            instance.is_forbidden = True
            instance.is_used = False
            instance.save()
        elif operation_type == 4:  # 恢复
            if instance.is_forbidden:
                raise serializers.ValidationError('操作失败，当前定线已禁用！')
            if instance.stash_flag and instance.is_used:  # 定线已使用才可恢复
                PlatFormInfo.objects.filter(pre_group__route_schema=instance).update(pre_group_id=None)
                CacheDevicePreRouteRelation.objects.filter(group__route_schema=instance).delete()
                instance.stash_flag = False
                instance.save()
        else:
            process_plats = validated_data.pop('process_plats', [])
            instance = super().update(instance, validated_data)
            if operation_type == 1:  # 暂存
                if instance.is_forbidden:
                    raise serializers.ValidationError('操作失败，当前定线已禁用！')
                PlatFormInfo.objects.filter(pre_group__route_schema=instance).update(pre_group_id=None)
                CacheDevicePreRouteRelation.objects.filter(group__route_schema=instance).delete()

                for item in process_plats:
                    plt_devices = item['plt_devices']
                    process_id = item['process_id']
                    try:
                        process = ProcessSection.objects.get(id=process_id)
                    except Exception:
                        continue
                    routing_plt = list(filter(lambda x: x['dp_type'] == 1, plt_devices))  # 定线机台
                    routing_device = list(filter(lambda x: x['dp_type'] == 2, plt_devices))  # 定线堆栈
                    plt_group = PlatformGroup.objects.filter(
                        route_schema=instance, process_id=process_id, group_type=1).first()
                    dev_group = PlatformGroup.objects.filter(
                        route_schema=instance, process_id=process_id, group_type=2).first()
                    if not plt_group:
                        plt_group = PlatformGroup.objects.create(
                            route_schema=instance,
                            group_ID='{}{}{}'.format('1', process.process_ID, instance.route_ID),
                            group_name='{}-{}-{}'.format(instance.route_name, process.process_name, 'AUTO'),
                            process_id=process_id,
                            group_type=1
                        )
                    if not dev_group:
                        dev_group = PlatformGroup.objects.create(
                            route_schema=instance,
                            group_ID='{}{}{}'.format('2', process.process_ID, instance.route_ID),
                            group_name='{}-{}-{}'.format(instance.route_name, process.process_name, 'BUFFER'),
                            process_id=process_id,
                            group_type=2
                        )
                    # 更新站台预定线组
                    PlatFormInfo.objects.filter(id__in=[plt['instance_id'] for plt in routing_plt]).update(pre_group=plt_group)
                    # 更新预定线堆栈组
                    cpr_list = []
                    for dev in routing_device:
                        dev_data = {'cache_device_id': dev['instance_id'], 'group': dev_group}
                        cpr_list.append(CacheDevicePreRouteRelation(**dev_data))
                    if cpr_list:
                        CacheDevicePreRouteRelation.objects.bulk_create(cpr_list)
                instance.stash_flag = True
                instance.save()
            else:  # 启用
                if instance.is_forbidden:
                    instance.is_used = True
                    instance.is_forbidden = False
                    instance.stash_flag = False
                    instance.save()
                else:
                    # 去掉旧定线和预定线
                    PlatFormInfo.objects.filter(group__route_schema=instance).update(group_id=None)
                    PlatFormInfo.objects.filter(pre_group__route_schema=instance).update(pre_group_id=None)
                    CacheDevicePreRouteRelation.objects.filter(group__route_schema=instance).delete()
                    CacheDeviceRouteRelation.objects.filter(group__route_schema=instance).delete()
                    for item in process_plats:
                        plt_devices = item['plt_devices']
                        process_id = item['process_id']
                        try:
                            process = ProcessSection.objects.get(id=process_id)
                        except Exception:
                            continue
                        routing_plt = list(filter(lambda x: x['dp_type'] == 1, plt_devices))  # 定线机台
                        routing_device = list(filter(lambda x: x['dp_type'] == 2, plt_devices))  # 定线堆栈
                        plt_group = PlatformGroup.objects.filter(
                            route_schema=instance, process_id=process_id, group_type=1).first()
                        dev_group = PlatformGroup.objects.filter(
                            route_schema=instance, process_id=process_id, group_type=2).first()
                        if not plt_group:
                            plt_group = PlatformGroup.objects.create(
                                route_schema=instance,
                                group_ID='{}{}{}'.format('1', process.process_ID, instance.route_ID),
                                group_name='{}-{}-{}'.format(instance.route_name, process.process_name, 'AUTO'),
                                process_id=process_id,
                                group_type=1
                            )
                        if not dev_group:
                            dev_group = PlatformGroup.objects.create(
                                route_schema=instance,
                                group_ID='{}{}{}'.format('2', process.process_ID, instance.route_ID),
                                group_name='{}-{}-{}'.format(instance.route_name, process.process_name, 'BUFFER'),
                                process_id=process_id,
                                group_type=2
                            )
                        # 更新站台定线组
                        PlatFormInfo.objects.filter(
                            id__in=[plt['instance_id'] for plt in routing_plt]).update(group=plt_group)
                        # 更新定线堆栈组
                        cpr_list = []
                        for dev in routing_device:
                            dev_data = {'cache_device_id': dev['instance_id'], 'group': dev_group}
                            cpr_list.append(CacheDeviceRouteRelation(**dev_data))
                        if cpr_list:
                            CacheDeviceRouteRelation.objects.bulk_create(cpr_list)
                    instance.is_used = True
                    instance.stash_flag = False
                    instance.save()
                    # # 更站台的设备组
                    # PlatFormInfo.objects.filter(group__route_schema=instance).update(group_id=None)
                    # PlatFormInfo.objects.filter(pre_group__route_schema=instance).update(group_id=F('pre_group_id'))
                    # # PlatFormInfo.objects.filter(id__in=list(PlatFormInfo.objects.filter(pre_group__route_schema=instance).values_list('id', flat=True))).update(group_id=F('pre_group_id'))
                    # # 去掉站台的预定线组
                    # PlatFormInfo.objects.filter(pre_group__route_schema=instance).update(pre_group_id=None)
                    # CacheDeviceRouteRelation.objects.filter(group__route_schema=instance).delete()
                    # pre_routing_devices = CacheDevicePreRouteRelation.objects.filter(group__route_schema=instance)
                    # # 新增堆栈的设备组
                    # cpr_list = []
                    # for pre_dev in pre_routing_devices:
                    #     pre_dev_dict = {'cache_device_id': pre_dev.cache_device_id, 'group': pre_dev.group}
                    #     cpr_list.append(CacheDeviceRouteRelation(**pre_dev_dict))
                    # if cpr_list:
                    #     CacheDeviceRouteRelation.objects.bulk_create(cpr_list)
                    # # 去掉堆栈的预定线组
                    # pre_routing_devices.delete()
                    # instance.is_used = True
                    # instance.stash_flag = False
                    # instance.save()
        return instance

    class Meta:
        model = RoutingSchema
        exclude = ('route_ID', )
        read_only_fields = COMMON_READ_ONLY_FIELDS


class PlatformGroupSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    def get_members(self, obj):
        if obj.group_type == 1:
            return obj.own_plts.values_list('platform_ID', flat=True)
        elif obj.group_type == 2:
            return CacheDeviceRouteRelation.objects.filter(group=obj).values_list('cache_device__device_ID', flat=True)
        else:
            return RestLocationRouteRelation.objects.filter(group=obj).values_list('rest_location__location_ID', flat=True)

    class Meta:
        model = PlatformGroup
        fields = '__all__'


# class ProcessCacheDeviceRelationSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ProcessCacheDeviceRelation
#         fields = ('process', 'in_task_threshold', 'out_task_threshold', 'task_priority')


class CacheDevicePartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CacheDevicePart
        fields = ('part_type', 'axis_no', 'slot_no', 'location_ID')


class CacheDeviceInfoSerializer(BaseModelSerializer):
    processes = serializers.SerializerMethodField()
    working_area_name = serializers.ReadOnlyField(source='working_area.area_name')
    route_schemas = serializers.SerializerMethodField()

    def get_processes(self, obj):
        return obj.device_process.values_list('process__process_name', flat=True)

    def get_route_schemas(self, obj):
        return set(CacheDeviceRouteRelation.objects.filter(
            cache_device=obj).values_list('group__route_schema__route_name', flat=True))

    class Meta:
        model = CacheDeviceInfo
        fields = '__all__'


class CacheDeviceInfoUpdateSerializer(BaseModelSerializer):
    device_ID = serializers.CharField(max_length=256, validators=[
        UniqueValidator(queryset=CacheDeviceInfo.objects.all(), message='堆栈ID已存在')])
    device_name = serializers.CharField(max_length=256, validators=[
        UniqueValidator(queryset=CacheDeviceInfo.objects.all(), message='堆栈名称已存在')])
    device_parts = CacheDevicePartSerializer(many=True, help_text="""[{"part_type": "部件类型 1:进 2:出", "axis_no":"轴号", "slot_no": "轨道号", "location_ID": "位置点ID"}]""")
    processes = serializers.PrimaryKeyRelatedField(queryset=ProcessSection.objects.all(), many=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        device_parts = ret['device_parts']
        sorted_device_parts = sorted(device_parts, key=lambda x: x['axis_no'])
        ret['device_parts'] = sorted_device_parts
        return ret

    @atomic()
    def create(self, validated_data):
        device_parts = validated_data.pop('device_parts', [])
        instance = super().create(validated_data)
        for dp in device_parts:
            dp['cache_device'] = instance
            CacheDevicePart.objects.create(**dp)
        row_num = validated_data['row_num']
        column_num = validated_data['column_num']
        layer_num = validated_data['layer_num']
        cs_list = []
        for r in range(1, row_num+1):
            for c in range(1, column_num+1):
                for ln in range(1, layer_num+1):
                    cs_data = {'equip_code': validated_data['device_name'],
                               'row': r, 'column': c, 'layer': ln}
                    cs_list.append(CacheDeviceStock(**cs_data))
        CacheDeviceStock.objects.bulk_create(cs_list)
        return instance

    @atomic()
    def update(self, instance, validated_data):
        if 'device_parts' in validated_data:
            device_parts = validated_data.pop('device_parts', [])
            instance.device_parts.all().delete()
            for dp in device_parts:
                dp['cache_device'] = instance
                CacheDevicePart.objects.create(**dp)
        processes = validated_data.get('processes', None)
        if processes:
            ins_dts = set(instance.processes.values_list('id', flat=True))
            u_dts = set([d.id for d in processes])
            uncommon_dts1 = u_dts & ins_dts
            uncommon_dts = ins_dts - uncommon_dts1
            if uncommon_dts:
                # 清除空花篮定线相关数据
                PlatformGroup.objects.filter(group_type=2, process_id__in=uncommon_dts).delete()
                if hasattr(instance, 'c_route'):
                    # instance.c_route.target_platforms.remove(*PlatFormInfo.objects.filter(process_id__in=uncommon_dts))
                    queryset = ProcessSection.objects.filter(
                        id__in=u_dts).filter(Q(upper_rail_type=2, upper_basket_type__in=(1, 3, 5)) |
                                             Q(lower_rail_type=2, lower_basket_type__in=(1, 3, 5)))
                    if not queryset:  # 不存空花篮时删除空花篮定线
                        instance.c_route.delete()
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = CacheDeviceInfo
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class LocationSerializer(BaseModelSerializer):
    location_name = serializers.CharField(max_length=256, validators=[UniqueValidator(
        queryset=Location.objects.all(), message='该休息位名称已存在')])

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class LocationRelationSerializer(serializers.ModelSerializer):
    location_name = serializers.ReadOnlyField(source='location.location_name')

    class Meta:
        model = LocationGroupRelation
        exclude = ('location_group', )


class LocationGroupSerializer(BaseModelSerializer):
    group_code = serializers.CharField(max_length=256, validators=[UniqueValidator(
        queryset=LocationGroup.objects.all(), message='该休息位组编号已存在')])
    group_name = serializers.CharField(max_length=256, validators=[UniqueValidator(
        queryset=LocationGroup.objects.all(), message='该休息位组名称已存在')])
    locationgrouprelation_set = LocationRelationSerializer(many=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        locationgrouprelation_set = ret['locationgrouprelation_set']
        ret['location_names'] = [i['location_name'] for i in locationgrouprelation_set]
        return ret

    def create(self, validated_data):
        l_groups = validated_data.pop('locationgrouprelation_set')
        instance = super().create(validated_data)
        for item in l_groups:
            LocationGroupRelation.objects.create(
                location=item['location'],
                location_group=instance,
                priority=item['priority']
            )
        return instance

    def update(self, instance, validated_data):
        l_groups = validated_data.pop('locationgrouprelation_set')
        instance = super().update(instance, validated_data)
        instance.locations.clear()
        for item in l_groups:
            LocationGroupRelation.objects.create(
                location=item['location'],
                location_group=instance,
                priority=item['priority']
            )
        return instance

    class Meta:
        model = LocationGroup
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class ThresholdDisplaySerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.group_name', default='')
    shunt_platform_group = serializers.SerializerMethodField()

    def get_shunt_platform_group(self, obj):
        return obj.shunt_platform_group.order_by('id').values_list('group_name', flat=True)

    class Meta:
        model = PlatFormInfo
        fields = ('id', 'platform_ID', 'platform_name', 'group_name', 'shunt_platform_group')
        read_only_fields = COMMON_READ_ONLY_FIELDS


class PlatFormImportSerializer(serializers.ModelSerializer):
    platform_ID = serializers.CharField(max_length=256)
    platform_name = serializers.CharField(max_length=256)
    desc = serializers.CharField(max_length=256)
    location_name = serializers.CharField(max_length=256)
    process = serializers.CharField(max_length=128)
    location_group = serializers.CharField(max_length=256, allow_null=True, allow_blank=True)
    wet_limit_groups = serializers.CharField(max_length=2048, allow_blank=True, allow_null=True, required=False)
    task_trigger_type = serializers.CharField(max_length=2048)
    is_dry_type = serializers.CharField(max_length=128, allow_null=True, allow_blank=True)

    class Meta:
        model = PlatFormInfo
        fields = ('platform_ID', 'platform_name', 'desc', 'location_name', 'process', 'q_time', 'pitch_time',
                  'location_group', 'task_trigger_type', 'up_task_trigger_threshold', 'down_task_trigger_threshold',
                  'is_dry_type', 'wet_limit_groups', 'wet_group_threshold', 'task_delay_time', 'task_priority')


class PlatFormExportSerializer(serializers.ModelSerializer):
    process_name = serializers.ReadOnlyField(source='process.process_name')
    working_area_name = serializers.ReadOnlyField(source='process.working_area.area_name', default=None)
    task_trigger_type_name = serializers.ReadOnlyField(source='get_task_trigger_type_display', default=None)
    platform_parts = PlatformPartSerializer(many=True)
    location_group_name = serializers.ReadOnlyField(source='location_group.group_name', default=None)
    rejected_platform_names = serializers.SerializerMethodField()
    wet_limit_group_names = serializers.SerializerMethodField()
    is_dry_type_flag = serializers.SerializerMethodField()

    def get_rejected_platform_names(self, obj):
        return '/'.join(obj.rejected_platform.values_list('platform_name', flat=True))

    def get_wet_limit_group_names(self, obj):
        return '/'.join(obj.wet_limit_groups.values_list('group_name', flat=True))

    def get_is_dry_type_flag(self, obj):
        if obj.is_dry_type:
            return '是'
        elif obj.is_dry_type is False:
            return '否'
        return ''

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        platform_parts = ret['platform_parts']
        ret['action1'] = ''
        ret['action2'] = ''
        ret['action3'] = ''
        ret['action4'] = ''
        for item in platform_parts:
            if item['axis_no'] == 1:
                ret['action1'] = item['part_type_name']
            if item['axis_no'] == 2:
                ret['action2'] = item['part_type_name']
            if item['axis_no'] == 3:
                ret['action3'] = item['part_type_name']
            if item['axis_no'] == 4:
                ret['action4'] = item['part_type_name']
        return ret

    class Meta:
        model = PlatFormInfo
        fields = ('platform_ID', 'platform_name', 'desc', 'location_name', 'process_name', 'q_time', 'pitch_time',
                  'location_group_name', 'task_trigger_type_name', 'up_task_trigger_threshold', 'down_task_trigger_threshold',
                  'is_dry_type_flag', 'wet_group_threshold', 'task_delay_time', 'task_priority',
                  'wet_limit_group_names', 'rejected_platform_names', 'working_area_name', 'platform_parts')