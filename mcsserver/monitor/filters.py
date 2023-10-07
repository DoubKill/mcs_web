# import django_filters
#
# from agv.models import Tasks
# from monitor.models import BasketTransportMonitor
#
#
# class BasketTransportMonitorFilter(django_filters.rest_framework.FilterSet):
#     st = django_filters.DateTimeFilter(field_name='begin_time', lookup_expr='gte', help_text="开始时间")
#     et = django_filters.DateTimeFilter(field_name='begin_time', lookup_expr='lte', help_text="结束时间")
#     process_id = django_filters.NumberFilter(field_name='platform__equip__process_id')
#     equip_id = django_filters.NumberFilter(field_name='platform__equip_id')
#
#     class Meta:
#         model = BasketTransportMonitor
#         fields = ('rfid', 'st', 'et', 'process_id', 'equip_id', 'platform_id')
import django_filters

from agv.models import Tasks
from monitor.models import AlarmLog


class TaskMonitorFilter(django_filters.rest_framework.FilterSet):
    task_no = django_filters.CharFilter(field_name='task_no', lookup_expr='icontains')
    st = django_filters.CharFilter(field_name='end_time', lookup_expr='gte')
    et = django_filters.CharFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = Tasks
        fields = ('task_no', 'agv_no', 'end_location', 'task_type', 'state', 'st', 'et')


class AlarmFilter(django_filters.rest_framework.FilterSet):
    st = django_filters.DateTimeFilter(field_name='last_updated_time', lookup_expr='gte')
    et = django_filters.DateTimeFilter(field_name='last_updated_time', lookup_expr='lte')
    alarm_desc = django_filters.CharFilter(field_name='alarm_desc', lookup_expr='icontains')

    class Meta:
        model = AlarmLog
        fields = ('st', 'et', 'alarm_desc')
