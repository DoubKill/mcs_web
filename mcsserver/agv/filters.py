import django_filters
from rest_framework.filters import OrderingFilter

from agv.models import Tasks, EnvCheckLocations, EnvCheckTasks, EnvTaskLocationRelation, EnvLocationCheckHistory


class EquipTaskTrackFilter(django_filters.rest_framework.FilterSet):
    st = django_filters.DateTimeFilter(field_name='end_time', lookup_expr='gte')
    et = django_filters.DateTimeFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = Tasks
        fields = ('st', 'et', 'platform_ID')


class EnvCheckLocationsFilter(django_filters.rest_framework.FilterSet):
    location_name = django_filters.CharFilter(field_name='location_name', help_text='位置点名称',
                                              lookup_expr='icontains')
    created_username = django_filters.CharFilter(field_name='created_user__username', help_text='创建人',
                                                 lookup_expr='icontains')
    created_time = django_filters.DateFilter(field_name='created_time__date', help_text='创建时间')
    last_updated_username = django_filters.CharFilter(field_name='last_updated_user__username', help_text='修改人',
                                                      lookup_expr='icontains')
    last_updated_time = django_filters.DateFilter(field_name='last_updated_time__date', help_text='修改时间')

    class Meta:
        model = EnvCheckLocations
        fields = ('location_name', 'created_username', 'created_time', 'last_updated_username',
                  'last_updated_time', 'working_area')


class EnvCheckLocationsOrderingFilter(OrderingFilter):

    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering:
            mapping = {
                'created_username': 'created_user__username',
                'last_updated_username': 'last_updated_user__username',
                # 在这里添加其他自定义字段名的映射关系
            }
            mapped_ordering = []
            for field in ordering:
                reverse = False
                if field.startswith('-'):
                    field = field[1:]
                    reverse = True
                mapped_field = mapping.get(field, field)
                if reverse:
                    mapped_field = '-' + mapped_field
                mapped_ordering.append(mapped_field)
            return mapped_ordering
        return ordering


class EnvCheckTasksFilter(django_filters.rest_framework.FilterSet):
    task_no = django_filters.CharFilter(field_name='task_no', lookup_expr='icontains')
    task_name = django_filters.CharFilter(field_name='task_name', lookup_expr='icontains')
    check_location_name = django_filters.CharFilter(method='filter_check_location_name')

    def filter_check_location_name(self, queryset, name, value):
        relates = EnvTaskLocationRelation.objects.filter(check_location__location_name__icontains=value).values_list('check_task_id', flat=True)
        return queryset.filter(id__in=relates)

    class Meta:
        model = EnvCheckTasks
        fields = ('task_no', 'task_name', 'working_area', 'task_trigger_type',
                  'check_location_name', 'is_used')


class EnvLocationCheckHistoryFilter(django_filters.rest_framework.FilterSet):
    st = django_filters.DateTimeFilter(field_name='created_time', lookup_expr='gte')
    et = django_filters.DateTimeFilter(field_name='created_time', lookup_expr='lte')

    class Meta:
        model = EnvLocationCheckHistory
        fields = ('location_name', 'check_state', 'task_no', 'working_area_name',
                  'agv_no', 'st', 'et', 'is_useful')