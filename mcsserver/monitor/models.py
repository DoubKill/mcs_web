from django.db import models


class AlarmLog(models.Model):
    alarm_type = models.PositiveIntegerField()  # 告警类型 1:站台 2:堆栈
    level = models.PositiveIntegerField()  # 级别
    alarm_desc = models.CharField(max_length=1024)  # 告警详情
    first_alarm_time = models.DateTimeField()  # 第一次告警的时间
    alarm_times = models.PositiveIntegerField()  # 重复次数
    last_updated_time = models.DateTimeField()  # 最后更新时间
    md5_data = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'dma_alarm_log'
        verbose_name_plural = verbose_name = '告警日志'


class DataSnapShot(models.Model):
    stock_type = models.IntegerField()  # 类型 1:AGV小车 2:堆栈
    stock_info = models.JSONField()  # 全站台/堆栈配置信息
    zz_info = models.JSONField()  # 在制信息
    zz_summary_info = models.JSONField()  # 在制统计信息
    created_time = models.DateTimeField()  # 创建时间
    tag = models.CharField(max_length=256, db_index=True)  # 标签

    class Meta:
        db_table = 'dma_snap_shot'
        verbose_name_plural = verbose_name = '在制快照'


class StockHistorySummary(models.Model):
    process_name = models.CharField(max_length=256)  # 工艺段名称
    route_name = models.CharField(max_length=256)  # 定线名称
    agv_trains_num = models.IntegerField(default=0)  # AGV物料车数
    cache_trains_num = models.IntegerField(default=0)  # 堆栈物料车数
    created_time = models.DateTimeField()  # 创建时间

    class Meta:
        db_table = 'dma_stock_history_summary'
        verbose_name_plural = verbose_name = '历史在制统计信息'