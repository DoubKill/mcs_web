from django.db import models

from basics.models import WorkArea
from user.models import AbstractEntity


class CacheDeviceStock(models.Model):
    equip_code = models.CharField(max_length=128, help_text='缓存设备编号', verbose_name='缓存设备编号')
    row = models.PositiveIntegerField(help_text='排', verbose_name='排')
    column = models.PositiveIntegerField(help_text='列', verbose_name='列')
    layer = models.PositiveIntegerField(help_text='层', verbose_name='层')
    in_processID = models.CharField(max_length=256, help_text='入库工艺段ID', verbose_name='入库工艺段ID', blank=True, null=True)
    in_material_type_name = models.CharField(max_length=128, help_text='入库物料类型', verbose_name='入库物料类型', blank=True, null=True)
    equipID = models.CharField(max_length=128, help_text='来源站台ID', verbose_name='来源站台ID', blank=True, null=True)
    output_time_consume = models.IntegerField(help_text='下料到入库耗时', verbose_name='下料到入库耗时', blank=True, null=True)
    storge_time = models.IntegerField(help_text='堆栈存储时间', verbose_name='堆栈存储时间', default=0, blank=True, null=True)
    q_time = models.IntegerField(help_text='物料超时时间(秒)', verbose_name='物料超时时间(秒)', blank=True, null=True)
    in_task_no = models.CharField(max_length=128, help_text='入库任务号', verbose_name='入库任务号', blank=True, null=True)
    # out_processID = models.CharField(max_length=256, help_text='出库工艺段ID', verbose_name='出库工艺段ID', blank=True, null=True)
    # out_material_type_name = models.CharField(max_length=128, help_text='出库物料类型', verbose_name='出库物料类型', blank=True, null=True)
    # out_task_no = models.CharField(max_length=128, help_text='出库任务号', verbose_name='出库任务号', blank=True, null=True)
    basket_num = models.IntegerField(help_text='库位花篮数', verbose_name='库位花篮数', default=0)
    layoff_time = models.CharField(max_length=19, help_text='下料时间', null=True, blank=True)

    class Meta:
        db_table = 'dam_cache_device_stock'
        verbose_name_plural = verbose_name = '缓存堆栈库存信息'


class CacheDeviceTasks(models.Model):
    device_ID = models.CharField(max_length=256)  # 堆栈ID
    material_type = models.CharField(max_length=256)  # 物料规格（设备组号）
    tag = models.CharField(max_length=256, blank=True, null=True)  # 标记
    task_type = models.IntegerField()  # 任务类型 1：入堆栈  2：出堆栈
    task_state = models.IntegerField()  # 任务状态 0:申请，1:创建，2: 结束
    traceback_state = models.IntegerField()  # 写入状态 0:未写入，1:写入成功
    request_allowed = models.IntegerField(blank=True, null=True)  # 0:不允许 1:允许
    created_time = models.DateTimeField()  # 创建时间
    end_time = models.DateTimeField(blank=True, null=True)  # 结束时间
    equip_no = models.CharField(max_length=256, blank=True, null=True)  # 来源站台

    class Meta:
        db_table = 'dam_cache_device_tasks'
        verbose_name_plural = verbose_name = '堆栈任务'
        indexes = [
                    models.Index(fields=['device_ID']),
                    models.Index(fields=['task_type']),
                    models.Index(fields=['task_state'])
        ]


class Tasks(models.Model):
    TASK_TYPE_CHOICE = (
        (1, '导航'),
        (2, '取货'),
        (3, '卸货'),
        (4, '取卸货'))  # 任务类型
    TASK_STATE_CHOICE = (
        (1, '已创建'),
        (2, '待下发'),
        (3, '已下发'),
        (4, '已派车'),
        (5, '已到达'),
        (6, '开始对接'),
        (7, '完成'),
        (8, '失败'),
        (9, '已取消'))  # 任务状态
    AXIS_ACTION_CHOICE = ((0, ''), (1, '取货'), (2, '卸货'))  # 轴动作类型
    task_no = models.CharField(max_length=128, help_text='任务号', verbose_name='任务号', unique=True)
    task_type = models.PositiveIntegerField(help_text='任务类型', verbose_name='任务类型', choices=TASK_TYPE_CHOICE)
    agv_no = models.IntegerField(help_text='AGV车号', verbose_name='AGV车号', blank=True, null=True)
    task_location_type = models.IntegerField(help_text='站台类型(1:站台 2:堆栈)', verbose_name='站台类型(1:站台 2:堆栈)', default=1)
    end_location = models.CharField(max_length=128, help_text='站台位置点', verbose_name='站台位置点')
    platform_ID = models.CharField(max_length=256, help_text='站台ID', verbose_name='站台ID', blank=True, null=True)
    platform_name = models.CharField(max_length=256, help_text='站台名称', verbose_name='站台名称', blank=True, null=True)
    process_name = models.CharField(max_length=256, help_text='工艺段名称', verbose_name='工艺段名称', blank=True, null=True)
    route_name = models.CharField(max_length=256, help_text='定线名称', verbose_name='定线名称', blank=True, null=True)
    priority = models.PositiveIntegerField(help_text='优先级', verbose_name='优先级', blank=True, null=True)
    state = models.PositiveIntegerField(help_text='任务执行状态', verbose_name='任务执行状态', choices=TASK_STATE_CHOICE)
    error_reason = models.CharField(max_length=2048, help_text='状态说明', verbose_name='状态说明', blank=True, null=True)
    created_time = models.DateTimeField(help_text='任务创建时间', verbose_name='任务创建时间', auto_now_add=True)
    last_updated_time = models.DateTimeField(help_text='任务修改时间', verbose_name='任务修改时间', auto_now=True)
    axis1_action = models.PositiveIntegerField(help_text='AGV轴1动作类型', verbose_name='AGV轴1动作类型', choices=AXIS_ACTION_CHOICE, blank=True, null=True)
    axis2_action = models.PositiveIntegerField(help_text='AGV轴2动作类型', verbose_name='AGV轴2动作类型', choices=AXIS_ACTION_CHOICE, blank=True, null=True)
    axis3_action = models.PositiveIntegerField(help_text='AGV轴3动作类型', verbose_name='AGV轴3动作类型', choices=AXIS_ACTION_CHOICE, blank=True, null=True)
    axis4_action = models.PositiveIntegerField(help_text='轴4动作类型', verbose_name='轴4动作类型', choices=AXIS_ACTION_CHOICE, blank=True, null=True)
    axis1_package_name = models.CharField(max_length=1024, help_text='AGV轴1包号', verbose_name='AGV轴1包号', blank=True, null=True)
    axis2_package_name = models.CharField(max_length=1024, help_text='AGV轴2包号', verbose_name='AGV轴2包号', blank=True, null=True)
    axis3_package_name = models.CharField(max_length=1024, help_text='AGV轴3包号', verbose_name='AGV轴3包号', blank=True, null=True)
    axis4_package_name = models.CharField(max_length=1024, help_text='AGV轴4包号', verbose_name='AGV轴4包号', blank=True, null=True)
    rcs_order_id = models.BigIntegerField(help_text='rcs订单ID', verbose_name='rcs订单ID', blank=True, null=True)
    change_time = models.DateTimeField(help_text='任务变更时间', verbose_name='任务变更时间', blank=True, null=True)
    active_time = models.DateTimeField(help_text='RCS激活订单时间', verbose_name='RCS激活订单时间', blank=True, null=True)
    dispatched_time = models.DateTimeField(help_text='RCS调度时间', verbose_name='RCS派车时间', blank=True, null=True)
    bind_time = models.DateTimeField(help_text='RCS派车时间', verbose_name='RCS派车时间', blank=True, null=True)
    begin_time = models.DateTimeField(help_text='AGV开始开始时间', verbose_name='AGV开始开始时间', blank=True, null=True)
    arrived_time = models.DateTimeField(help_text='AGV到达时间', verbose_name='小车到达时间', blank=True, null=True)
    begin_act_time = models.DateTimeField(help_text='开始对接时间', verbose_name='开始对接时间', blank=True, null=True)
    end_time = models.DateTimeField(help_text='完成时间', verbose_name='完成时间', blank=True, null=True)
    error_time = models.DateTimeField(help_text='error时间', verbose_name='error时间', blank=True, null=True)
    origin_platform_ID = models.CharField(max_length=256, help_text='来源站台ID', verbose_name='来源站台ID', blank=True, null=True)
    origin_platform_name = models.CharField(max_length=256, help_text='来源站台名称', verbose_name='来源站台名称', blank=True, null=True)
    receive_time = models.DateTimeField(help_text='接料完成时间', verbose_name='接料完成时间', blank=True, null=True)
    dz_group_no = models.CharField(max_length=256, blank=True, null=True)  # 堆栈取、卸货包号（设备组号）

    @property
    def state_name(self):
        return self.get_state_display()

    @property
    def task_type_name(self):
        return self.get_task_type_display()

    class Meta:
        db_table = 'dma_tasks'
        verbose_name_plural = verbose_name = 'MCS任务表'
        indexes = [
            models.Index(fields=['agv_no']),
            models.Index(fields=['state']),
            models.Index(fields=['task_type']),
            models.Index(fields=['platform_ID']),
            models.Index(fields=['process_name'])
        ]


class RCSCommand(models.Model):
    OPERATION_TYPE_CHOICE = ((1, '取消订单'), (2, '变更终点'), (3, '强制完成'))
    TASK_OPERATION_TYPE_STATE_CHOICE = ((1, '创建'), (2, '完成'), (3, '失败'))
    AXIS_ACTION_CHOICE = ((1, '取货'), (2, '卸货'))  # 轴动作类型
    task = models.ForeignKey(Tasks, help_text='MCS任务', verbose_name='MCS任务', on_delete=models.CASCADE)
    task_no = models.CharField(max_length=128, help_text='任务号', verbose_name='任务号')
    command_type = models.PositiveIntegerField(help_text='操作类型', verbose_name='操作类型', choices=OPERATION_TYPE_CHOICE)
    current_retry_times = models.PositiveIntegerField(help_text='当前重试次数', verbose_name='当前重试次数', default=0)
    last_retry_time = models.DateTimeField(help_text='上次重试时间', verbose_name='上次重试时间', blank=True, null=True)
    error_reason = models.CharField(max_length=2048, help_text='失败原因', verbose_name='失败原因', blank=True, null=True)
    created_time = models.DateTimeField(help_text='创建时间', verbose_name='创建时间', auto_now_add=True)
    last_updated_time = models.DateTimeField(help_text='修改时间', verbose_name='修改时间', auto_now=True)
    send_data = models.JSONField(help_text='发送数据', verbose_name='发送数据',blank=True, null=True)
    task_delay_time = models.IntegerField(help_text='任务延迟时间', verbose_name='任务延迟时间', default=0)

    class Meta:
        db_table = 'dma_tasks_command'
        verbose_name_plural = verbose_name = 'RCS订单操作'


class EnvIndicators(models.Model):
    indicator_type = models.PositiveIntegerField()  # 1:温度 2:湿度 3:0.3微米离子数 4:0.5微米离子数 5:1微米离子数 6:3微米离子数 7:5微米离子数
    warning_value = models.FloatField()  # 预警值
    alarm_value = models.FloatField()  # 告警值

    class Meta:
        db_table = 'env_indicators'
        verbose_name_plural = verbose_name = '环境检测指标点'


class EnvCheckLocations(AbstractEntity):
    location_name = models.CharField(max_length=256, help_text='位置点名称', verbose_name='位置点名称', unique=True)
    working_area = models.ForeignKey(WorkArea, help_text='工作区id', verbose_name='工作区id', on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.location_name)

    class Meta:
        db_table = "env_check_locations"
        verbose_name_plural = verbose_name = '环境检测位置点'


class EnvCheckTasks(AbstractEntity):
    task_no = models.CharField(max_length=256, help_text='任务编号', verbose_name='任务编号', unique=True)
    task_name = models.CharField(max_length=256, help_text='任务名称', verbose_name='任务名称', unique=True)
    working_area = models.ForeignKey(WorkArea, help_text='工作区id', verbose_name='工作区id', on_delete=models.PROTECT)
    task_trigger_type = models.PositiveIntegerField()  # 1:单次 2:每日
    trigger_time = models.JSONField()
    is_used = models.BooleanField(help_text='是否启用', verbose_name='是否启用', default=True)
    locations = models.ManyToManyField(EnvCheckLocations, through='EnvTaskLocationRelation')

    class Meta:
        db_table = 'env_check_tasks'
        verbose_name_plural = verbose_name = '环境检测任务'


class EnvTaskLocationRelation(models.Model):
    check_location = models.ForeignKey(EnvCheckLocations, on_delete=models.CASCADE)
    check_task = models.ForeignKey(EnvCheckTasks, on_delete=models.CASCADE)
    ordering = models.IntegerField()

    class Meta:
        db_table = "env_task_location_relation"
        verbose_name_plural = verbose_name = '检测任务位置关系表'


class EnvLocationCheckHistory(models.Model):
    check_no = models.CharField(max_length=256)  # 下发单号（属于同一任务下发的单号一样）
    location_name = models.CharField(max_length=256)  # 位置点
    task_no = models.CharField(max_length=256)  # 任务号
    working_area_name = models.CharField(max_length=256)  # 工作区名称
    state = models.PositiveIntegerField()  # 状态 0：下发失败 1：已下发 2：已上报
    agv_no = models.CharField(max_length=256)  # AGV车号
    created_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    report_time = models.DateTimeField(blank=True, null=True)  # 上报时间
    indicator_value_1 = models.FloatField(blank=True, null=True)  # 温度
    indicator_value_2 = models.FloatField(blank=True, null=True)  # 湿度
    indicator_value_3 = models.FloatField(blank=True, null=True)  # 0.3微米离子数
    indicator_value_4 = models.FloatField(blank=True, null=True)  # 0.5微米离子数
    indicator_value_5 = models.FloatField(blank=True, null=True)  # 1微米离子数
    indicator_value_6 = models.FloatField(blank=True, null=True)  # 3微米离子数
    indicator_value_7 = models.FloatField(blank=True, null=True)  # 5微米离子数
    check_state = models.PositiveIntegerField()  # 状态 1：正常 2：告警 3：报警
    is_useful = models.BooleanField(default=True)  # 是否有效

    class Meta:
        db_table = "env_location_check_history"
        verbose_name_plural = verbose_name = '检测点结果报表'