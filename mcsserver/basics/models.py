from django.db import models

# Create your models here.
from user.models import AbstractEntity

BASKET_TYPE_CHOICE = (
        (1, '空叠片盒'),
        (2, '满叠片盒'),
        (3, '空湿花篮'),
        (4, '满湿花篮'),
        (5, '空干花篮'),
        (6, '满干花篮')
    )


class Configuration(AbstractEntity):
    key = models.CharField(max_length=64, blank=True, null=True)
    value = models.CharField(max_length=1024, blank=True, null=True)
    desc = models.CharField(max_length=256, blank=True, null=True)
    value_type = models.CharField(max_length=256, blank=True, null=True)
    choices = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'bdm_configuration'
        verbose_name_plural = verbose_name = '全局配置'


class GlobalCodeType(AbstractEntity):
    """公共代码类型表"""
    type_no = models.CharField(max_length=64, help_text='类型编号', verbose_name='类型编号', unique=True)
    type_name = models.CharField(max_length=64, help_text='类型名称', verbose_name='类型名称')
    description = models.CharField(max_length=256, blank=True, null=True, help_text='说明', verbose_name='说明')

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'bdm_global_code_type'
        verbose_name_plural = verbose_name = '公共代码类型'


class GlobalCode(AbstractEntity):
    """公共代码表"""
    global_type = models.ForeignKey('GlobalCodeType', models.PROTECT, related_name="global_codes",
                                    help_text='全局类型ID', verbose_name='全局类型ID')
    global_no = models.CharField(max_length=64, help_text='公共代码编号', verbose_name='公共代码编号', unique=True)
    global_name = models.CharField(max_length=64, help_text='公用代码名称', verbose_name='公用代码名称')
    description = models.CharField(max_length=256, blank=True, null=True,
                                   help_text='说明', verbose_name='说明')
    # use_flag = models.BooleanField(help_text='是否启用', verbose_name='是否启用', default=True)

    def __str__(self):
        return self.global_name

    class Meta:
        db_table = 'bdm_global_code'
        verbose_name_plural = verbose_name = '公共代码'


class AgvType(models.Model):
    type_ID = models.CharField(max_length=256)
    type_name = models.CharField(max_length=256)

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'bdm_agv_type'
        verbose_name_plural = verbose_name = 'AGV类型'


class WorkArea(AbstractEntity):
    """工作区表"""
    area_ID = models.CharField(max_length=64, help_text='工作区ID', verbose_name='工作区ID', unique=True)
    area_name = models.CharField(max_length=64, help_text='工作区名称', verbose_name='工作区名称', unique=True)
    description = models.CharField(max_length=256, blank=True, null=True, help_text='描述', verbose_name='描述')
    rcs_address = models.CharField(max_length=256, blank=True, null=True, help_text='RCS地址', verbose_name='RCS地址')
    agv_type = models.ForeignKey(AgvType, blank=True, null=True, on_delete=models.SET_NULL)  # AGV类型

    class Meta:
        db_table = 'bdm_work_area'
        verbose_name_plural = verbose_name = '工作区'


class ProcessSection(AbstractEntity):
    RAIL_TYPE_CHOICE = (
        (1, '上料'),
        (2, '下料'),
    )
    process_ID = models.CharField(max_length=256, help_text='工艺段ID', verbose_name='工艺段ID', unique=True)
    process_name = models.CharField(max_length=128, help_text='工艺段名称', verbose_name='工艺段名称', unique=True)
    ordering = models.IntegerField(help_text='顺序', verbose_name='顺序', unique=True)
    working_area = models.ForeignKey('WorkArea', help_text='工作区id', verbose_name='工作区id', on_delete=models.PROTECT, db_constraint=False)
    upper_rail_type = models.IntegerField(help_text='上层轨道上下料类型', verbose_name='上层轨道上下料类型'
                                          , choices=RAIL_TYPE_CHOICE, null=True)
    upper_basket_type = models.IntegerField(help_text='上层花篮类型', verbose_name='上层花篮类型'
                                            , choices=BASKET_TYPE_CHOICE, null=True)
    lower_rail_type = models.IntegerField(help_text='下层轨道上下料类型', verbose_name='下层轨道上下料类型',
                                          choices=RAIL_TYPE_CHOICE, null=True)
    lower_basket_type = models.IntegerField(help_text='下层花篮类型', verbose_name='下层花篮类型'
                                            , choices=BASKET_TYPE_CHOICE, null=True)
    source_process = models.ForeignKey('self', help_text='源工艺段id', verbose_name='源工艺段id', on_delete=models.SET_NULL,
                                       blank=True, null=True, related_name='r_sources')
    target_process = models.ForeignKey('self', help_text='目标工艺段id', verbose_name='目标工艺段id', on_delete=models.SET_NULL,
                                       blank=True, null=True, related_name='r_targets')
    cell_numbers = models.IntegerField(help_text='单车电池片数量', verbose_name='单车电池片数量')
    q_time = models.IntegerField(help_text='物料超时时间(秒)', verbose_name='物料超时时间(秒)')
    warning_time = models.IntegerField(help_text='预警时间(秒)', verbose_name='预警时间(秒)')
    pitch_time = models.IntegerField(help_text='节拍(秒)', verbose_name='节拍(秒)')
    single_slot_num = models.IntegerField(help_text='单轴花篮数', verbose_name='单轴花篮数')

    def __str__(self):
        return "{}".format(self.process_name)

    class Meta:
        db_table = "bdm_process_section"
        verbose_name_plural = verbose_name = '工艺段'


class Location(AbstractEntity):
    location_name = models.CharField(max_length=256, help_text='位置点名称', verbose_name='位置点名称', unique=True)
    is_used = models.BooleanField(help_text='是否启用', verbose_name='是否启用', default=True)
    is_synced = models.BooleanField(help_text='是否同步到RCS', verbose_name='是否同步到RCS', default=False)

    def __str__(self):
        return "{}".format(self.location_name)

    class Meta:
        db_table = "bdm_location"
        verbose_name_plural = verbose_name = '休息位'


class LocationGroup(AbstractEntity):
    group_code = models.CharField(max_length=256, help_text='休息位组编号', verbose_name='休息位组编号', unique=True)
    group_name = models.CharField(max_length=256, help_text='休息位组名称', verbose_name='休息位组名称', unique=True)
    locations = models.ManyToManyField(Location, through='LocationGroupRelation')

    def __str__(self):
        return "{}".format(self.group_name)

    class Meta:
        db_table = "bdm_location_group"
        verbose_name_plural = verbose_name = '休息位组'


class LocationGroupRelation(models.Model):
    location = models.ForeignKey(Location, help_text='休息位', verbose_name='休息位', on_delete=models.PROTECT)
    location_group = models.ForeignKey(LocationGroup, help_text='休息位组', verbose_name='休息位组', on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(help_text='优先级', verbose_name='优先级')

    class Meta:
        db_table = "bdm_location_group_relation"
        verbose_name_plural = verbose_name = '休息位组关系表'


  # 已弃用
class RestLocation(AbstractEntity):
    location_ID = models.CharField(max_length=256, help_text='位置ID', verbose_name='位置ID')
    location_code = models.CharField(max_length=256, help_text='位置点编号', verbose_name='位置点名称')
    location_name = models.CharField(max_length=256, help_text='位置点名称', verbose_name='位置点名称')
    desc = models.CharField(max_length=256, help_text='备注', verbose_name='备注', blank=True, null=True)
    working_area = models.ForeignKey('WorkArea', help_text='工作区ID', verbose_name='工作区ID', on_delete=models.PROTECT, db_constraint=False)
    is_used = models.BooleanField(help_text='是否启用', verbose_name='是否启用', default=True)
    processes = models.ManyToManyField(ProcessSection, through='ProcessRestLocationRelation')

    def __str__(self):
        return "{}".format(self.location_name)

    class Meta:
        db_table = "bdm_rest_location"
        verbose_name_plural = verbose_name = '休息停靠位'


  # 已弃用
class ProcessRestLocationRelation(models.Model):
    rest_location = models.ForeignKey(RestLocation, help_text='休息停靠位id', verbose_name='休息停靠位id', on_delete=models.CASCADE)
    process = models.ForeignKey(ProcessSection, help_text='工艺段id', verbose_name='工艺段id', on_delete=models.CASCADE)

    class Meta:
        db_table = "bdm_process_rest_location_relation"
        verbose_name_plural = verbose_name = '工艺段休息停靠位关系表'


class PlatFormInfo(AbstractEntity):
    PLATFORM_TYPE_CHOICE = (
        (1, '上料'),
        (2, '下料'),
        (3, '上下料')
    )
    TASK_TRIGGER_TYPE_CHOICE = (
        (0, '关闭'),
        (1, '以上料阈值'),
        (2, '以下料阈值'),
    )
    platform_ID = models.CharField(max_length=256, help_text='站台ID', verbose_name='站台ID', unique=True)
    platform_name = models.CharField(max_length=256, help_text='站台名称', verbose_name='站台名称', unique=True)
    desc = models.CharField(max_length=256, help_text='站台描述', verbose_name='站台描述')
    process = models.ForeignKey(ProcessSection, help_text='工艺段id', on_delete=models.PROTECT,
                                related_name='process_platforms')
    platform_type = models.PositiveIntegerField(help_text='站台类型', verbose_name='站台类型', choices=PLATFORM_TYPE_CHOICE)
    q_time = models.IntegerField(help_text='物料超时时间(秒)', verbose_name='物料超时时间(秒)')
    pitch_time = models.IntegerField(help_text='节拍', verbose_name='物料超时时间(秒)')
    is_used = models.BooleanField(help_text='是否启用', verbose_name='是否启用', default=True)

    location_name = models.CharField(max_length=256, help_text='位置点名称', verbose_name='位置点名称', blank=True, null=True)

    rejected_platform = models.ManyToManyField('self', help_text='互斥站台id列表', verbose_name='互斥站台id列表',
                                               blank=True, db_table='shunt_reject_platform_relation')
    rejected_threshold = models.IntegerField(help_text='互斥站台阈值', verbose_name='互斥站台阈值', blank=True, null=True)

    is_dry_type = models.BooleanField(help_text='是否干式设备', verbose_name='是否干式设备', null=True)
    wet_limit_groups = models.ManyToManyField('PlatformGroup', help_text='湿区设备限制组id列表', verbose_name='湿区设备限制组id列表',
                                              db_table='wet_platform_group_relation', blank=True, related_name='wet_plts')
    wet_group_threshold = models.IntegerField(help_text='湿式设备组阈值', verbose_name='湿式设备组阈值', blank=True, null=True)

    shunt_platform_group = models.ManyToManyField('PlatformGroup', help_text='分流设备组id列表', verbose_name='分流设备组id列表',
                                                  db_table='shunt_platform_group_relation', blank=True, related_name='shunt_plts')
    shunt_threshold = models.IntegerField(help_text='分流阈值', verbose_name='分流阈值', blank=True, null=True)

    task_trigger_type = models.IntegerField(help_text='任务触发方式', verbose_name='任务触发方式', choices=TASK_TRIGGER_TYPE_CHOICE)
    up_task_trigger_threshold = models.IntegerField(help_text='上料阈值', verbose_name='上料阈值', blank=True, null=True)
    down_task_trigger_threshold = models.IntegerField(help_text='下料阈值', verbose_name='下料阈值', blank=True, null=True)

    task_priority = models.IntegerField(help_text='任务优先级', verbose_name='任务优先级', default=1)
    task_delay_time = models.IntegerField(help_text='任务延迟时间（S）', verbose_name='任务延迟时间（S）', default=0)
    group = models.ForeignKey('PlatformGroup', help_text='归属设备组id', verbose_name='归属设备组id',
                              on_delete=models.SET_NULL, related_name='own_plts', blank=True, null=True)
    pre_group = models.ForeignKey('PlatformGroup', help_text='预定线归属设备组id', verbose_name='预定线归属设备组id',
                                  on_delete=models.SET_NULL, related_name='own_pre_plts', blank=True, null=True)
    location_group = models.ForeignKey('LocationGroup', help_text='休息位组id', verbose_name='休息位组id',
                                       on_delete=models.PROTECT, related_name='lc_plts', blank=True, null=True)

    def source_plt_group_name(self):
        """物料来源(站台设备组)"""
        if not self.group:
            return None
        obj = PlatformGroup.objects.filter(
            route_schema=self.group.route_schema,
            process=self.process.source_process,
            group_type=1).first()
        if obj:
            return obj.group_name

    def source_cache_group_name(self):
        """物料来源(堆栈设备组)"""
        if not self.group:
            return None
        obj = PlatformGroup.objects.filter(
            route_schema=self.group.route_schema,
            process=self.process.source_process,
            group_type=2).first()
        if obj:
            return obj.group_name

    def target_plt_group_name(self):
        """物料去向(站台设备组)"""
        if not self.group:
            return None
        obj = PlatformGroup.objects.filter(
            route_schema=self.group.route_schema,
            process=self.process.target_process,
            group_type=1).first()
        if obj:
            return obj.group_name

    def target_cache_group_name(self):
        """物料去向(堆栈设备组)"""
        if not self.group:
            return None
        obj = PlatformGroup.objects.filter(
            route_schema=self.group.route_schema,
            process=self.process,
            group_type=2).first()
        if obj:
            return obj.group_name

    def __str__(self):
        return "{}".format(self.platform_name)

    class Meta:
        db_table = "bdm_platform_info"
        verbose_name_plural = verbose_name = '工艺站台配置'


class PlatFormRealInfo(models.Model):
    STATE_CHOICE = (
        (1, '无生产计划'),
        (2, '计划停机'),
        (3, '工程试验'),
        (4, '正常生产'),
        (5, '设备缺料'),
        (6, '机台故障')
    )
    platform_info = models.OneToOneField(PlatFormInfo, help_text='站台id', verbose_name='站台id', on_delete=models.CASCADE,
                                         related_name='platform_real_info')
    upper_basket_num = models.IntegerField(help_text='上料花篮数', verbose_name='上料花篮数', blank=True, null=True)
    lower_basket_num = models.IntegerField(help_text='下料花篮数', verbose_name='下料花篮数', blank=True, null=True)
    upper_basket_changed_time = models.DateTimeField(help_text='上料花篮变更时间', verbose_name='上料花篮变更时间', blank=True, null=True)
    lower_basket_changed_time = models.DateTimeField(help_text='下料花篮变更时间', verbose_name='下料花篮变更时间', blank=True, null=True)
    upper_rail_state = models.IntegerField(help_text='上料屏蔽 1:屏蔽 0:未屏蔽', verbose_name='上料屏蔽 1:屏蔽 0:未屏蔽', blank=True, null=True)
    lower_rail_state = models.IntegerField(help_text='下料屏蔽 1:屏蔽 0:未屏蔽', verbose_name='下料屏蔽 1:屏蔽 0:未屏蔽', blank=True, null=True)
    state = models.IntegerField(help_text='机台状态', verbose_name='机台状态', default=5, choices=STATE_CHOICE)
    dock_status = models.IntegerField(help_text='对接状态:agv写入机台的id', verbose_name='对接状态', default=0)
    begin_time = models.DateTimeField(blank=True, null=True)  # 开始读WCS时间
    last_updated_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    is_connected = models.BooleanField(default=True)

    class Meta:
        db_table = "bdm_platform_real_info"
        verbose_name_plural = verbose_name = '工艺站台实时信息'


class PlatformPart(AbstractEntity):
    PART_TYPE_CHOICE = (
        (1, 'AGV取货'),
        (2, 'AGV卸货')
    )
    platform_info = models.ForeignKey(PlatFormInfo, help_text='站台id', verbose_name='站台id', on_delete=models.CASCADE,
                                      related_name='platform_parts')
    axis_no = models.PositiveIntegerField(help_text='轴号', verbose_name='轴号')
    slot_no = models.CharField(max_length=256, help_text='轨道号', verbose_name='轨道号')
    part_type = models.PositiveIntegerField(help_text='部件类型', verbose_name='部件类型', choices=PART_TYPE_CHOICE, null=True)
    # basket_type = models.IntegerField(help_text='花篮类型', verbose_name='花篮类型',
    #                                   choices=BASKET_TYPE_CHOICE)
    location_ID = models.CharField(max_length=256, help_text='位置点ID', verbose_name='位置点ID', null=True)
    is_used = models.BooleanField(help_text='是否启用', verbose_name='是否启用', default=True)

    class Meta:
        db_table = 'bdm_platform_part'
        verbose_name_plural = verbose_name = '站台部件'


class CacheDeviceInfo(AbstractEntity):
    device_ID = models.CharField(max_length=256, help_text='站台ID', verbose_name='站台ID', unique=True)
    device_name = models.CharField(max_length=256, help_text='站台名称', verbose_name='站台名称', unique=True)
    desc = models.CharField(max_length=256, help_text='站台描述', verbose_name='站台描述')
    in_location_name = models.CharField(max_length=256, help_text='进料位置点名称', verbose_name='进料位置点名称')
    out_location_name = models.CharField(max_length=256, help_text='出料位置点名称', verbose_name='出料位置点名称')
    working_area = models.ForeignKey('WorkArea', help_text='工作区id', verbose_name='工作区id', on_delete=models.PROTECT, db_constraint=False)
    allow_task_num = models.IntegerField(help_text='允许任务数', verbose_name='允许任务数')
    task_delay_time = models.IntegerField(help_text='任务延迟时间（S）', verbose_name='任务延迟时间（S）', default=0)
    row_num = models.IntegerField(help_text='排数', verbose_name='排数', default=1)
    column_num = models.IntegerField(help_text='层数', verbose_name='层数', default=1)
    layer_num = models.IntegerField(help_text='列数', verbose_name='列数', default=1)
    processes = models.ManyToManyField(ProcessSection, through='ProcessCacheDeviceRelation')
    task_priority = models.IntegerField(help_text='任务优先级', verbose_name='任务优先级', default=5)
    storage_num = models.IntegerField(help_text='单库位可存放花篮数', verbose_name='单库位可存放花篮数', default=5)
    in_is_used = models.BooleanField(help_text='进料启用', verbose_name='进料启用', default=True)
    out_is_used = models.BooleanField(help_text='出料启用', verbose_name='出料启用', default=True)
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.device_name)

    class Meta:
        db_table = "bdm_cache_device_info"
        verbose_name_plural = verbose_name = '缓存堆栈配置'


class ProcessCacheDeviceRelation(AbstractEntity):
    cache_device = models.ForeignKey(CacheDeviceInfo, help_text='堆栈id', verbose_name='堆栈id', on_delete=models.CASCADE,
                                     related_name='device_process')
    process = models.ForeignKey(ProcessSection, help_text='工艺段id', verbose_name='工艺段id', on_delete=models.CASCADE)
    # in_task_threshold = models.IntegerField(help_text='进料阈值', verbose_name='进料阈值')
    # out_task_threshold = models.IntegerField(help_text='出料阈值', verbose_name='出料阈值')
    # task_priority = models.IntegerField(help_text='任务优先级', verbose_name='任务优先级', default=1)

    class Meta:
        db_table = 'bdm_process_cache_device_relation'
        verbose_name_plural = verbose_name = '堆栈工艺段关系表'


class CacheDevicePart(AbstractEntity):
    PART_TYPE_CHOICE = (
        (1, 'AGV取货'),
        (2, 'AGV卸货')
    )
    cache_device = models.ForeignKey(CacheDeviceInfo, help_text='堆栈id', verbose_name='堆栈id', on_delete=models.CASCADE,
                                     related_name='device_parts')
    part_type = models.PositiveIntegerField(help_text='部件类型', verbose_name='部件类型', choices=PART_TYPE_CHOICE)
    axis_no = models.PositiveIntegerField(help_text='轴号', verbose_name='轴号')
    slot_no = models.CharField(max_length=256, help_text='轨道号', verbose_name='轨道号')
    location_ID = models.CharField(max_length=256, help_text='位置点ID', verbose_name='位置点ID')
    is_used = models.BooleanField(help_text='是否启用', verbose_name='是否启用', default=True)

    class Meta:
        db_table = 'bdm_cache_device_part'
        verbose_name_plural = verbose_name = '堆栈部件'


class RoutingSchema(AbstractEntity):
    route_ID = models.CharField(max_length=256, help_text='定线ID', verbose_name='定线ID', unique=True)
    route_name = models.CharField(max_length=256, help_text='定线名称', verbose_name='定线名称', unique=True)
    is_used = models.BooleanField(help_text='是否正在使用', verbose_name='是否正在使用', default=False)
    is_forbidden = models.BooleanField(help_text='是否禁用', verbose_name='是否禁用', default=False)
    stash_flag = models.BooleanField(help_text='是否暂存标记', verbose_name='是否暂存标记', default=True)

    class Meta:
        db_table = 'bdm_route_schema'
        verbose_name_plural = verbose_name = '站台定线'


class PlatformGroup(AbstractEntity):
    GROUP_TYPE_CHOICE = (
        (1, '站台组'),
        (2, '堆栈组'),
        (3, '休息位组')
    )
    route_schema = models.ForeignKey(RoutingSchema, help_text='定线id', verbose_name='定线id', on_delete=models.CASCADE,
                                     related_name='r_groups')
    group_ID = models.CharField(max_length=256, help_text='设备组ID', verbose_name='设备组ID', unique=True)
    group_name = models.CharField(max_length=256, help_text='设备组名称', verbose_name='设备组名称', unique=True)
    process = models.ForeignKey(ProcessSection, help_text='工艺段id', on_delete=models.CASCADE,
                                related_name='process_groups')
    group_type = models.IntegerField(help_text='站台组类型', verbose_name='站台组类型', choices=GROUP_TYPE_CHOICE)
    maximum = models.IntegerField(help_text='最大值', verbose_name='最大值', default=100)
    minimum = models.IntegerField(help_text='最小值', verbose_name='最小值', default=0)
    warning_maximum = models.IntegerField(help_text='预警最大值', verbose_name='预警最大值', default=100)
    warning_minimum = models.IntegerField(help_text='预警最小值', verbose_name='预警最小值', default=0)

    class Meta:
        db_table = 'bdm_platform_group'
        verbose_name_plural = verbose_name = '设备组'
        unique_together = ('route_schema', 'process', 'group_type')


class CacheDeviceRouteRelation(AbstractEntity):
    cache_device = models.ForeignKey(CacheDeviceInfo, help_text='缓存堆栈id', verbose_name='缓存堆栈id', on_delete=models.PROTECT)
    group = models.ForeignKey(PlatformGroup, help_text='站台定线组id', verbose_name='站台定线组id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bdm_route_cache_device_relation'
        verbose_name_plural = verbose_name = '堆栈定线关系表'


class CacheDevicePreRouteRelation(AbstractEntity):
    cache_device = models.ForeignKey(CacheDeviceInfo, help_text='缓存堆栈id', verbose_name='缓存堆栈id', on_delete=models.PROTECT)
    group = models.ForeignKey(PlatformGroup, help_text='站台定线组id', verbose_name='站台定线组id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bdm_pre_route_cache_device_relation'
        verbose_name_plural = verbose_name = '堆栈预定线关系表'


class RestLocationRouteRelation(AbstractEntity):
    rest_location = models.ForeignKey(RestLocation, help_text='休息位id', verbose_name='休息位id', on_delete=models.PROTECT)
    group = models.ForeignKey(PlatformGroup, help_text='站台定线组id', verbose_name='站台定线组id', on_delete=models.CASCADE,
                              related_name='r_rls')
    priority = models.IntegerField(help_text='缓存位优先级', verbose_name='缓存位优先级', default=5)

    class Meta:
        db_table = 'bdm_route_rest_location_relation'
        verbose_name_plural = verbose_name = '休息位定线关系表'


class EmptyBasketRouteSchema(AbstractEntity):
    route_ID = models.CharField(max_length=256, help_text='定线ID', verbose_name='定线ID', unique=True)
    route_name = models.CharField(max_length=256, help_text='定线名称', verbose_name='定线名称', unique=True)
    platform_info = models.OneToOneField(PlatFormInfo, help_text='站台id', verbose_name='站台id',
                                         on_delete=models.CASCADE, related_name='p_route')
    target_platforms = models.ManyToManyField(PlatFormInfo, db_table='bdm_route_platform_relation',
                                              related_name='p_etrs')

    class Meta:
        db_table = 'bdm_empty_route_schema'
        verbose_name_plural = verbose_name = '空花篮站台定线'


class EmptyCacheRouteSchema(AbstractEntity):
    route_ID = models.CharField(max_length=256, help_text='定线ID', verbose_name='定线ID', unique=True)
    route_name = models.CharField(max_length=256, help_text='定线名称', verbose_name='定线名称', unique=True)
    cache_info = models.OneToOneField(CacheDeviceInfo, help_text='堆栈id', verbose_name='堆栈id',
                                      on_delete=models.CASCADE, related_name='c_route')
    target_platforms = models.ManyToManyField(PlatFormInfo, db_table='bdm_cache_route_platform_relation',
                                              related_name='p_cetrs')

    class Meta:
        db_table = 'bdm_empty_cache_route_schema'
        verbose_name_plural = verbose_name = '空花篮堆栈定线'