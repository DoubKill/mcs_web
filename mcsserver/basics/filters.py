import django_filters
from rest_framework.filters import OrderingFilter

from basics.models import GlobalCodeType, GlobalCode, ProcessSection, PlatFormInfo, RestLocation, PlatformGroup, \
    CacheDeviceInfo, WorkArea, CacheDeviceRouteRelation, RestLocationRouteRelation, Location, LocationGroupRelation, \
    LocationGroup


class GlobalCodeTypeFilter(django_filters.rest_framework.FilterSet):
    type_no = django_filters.CharFilter(field_name='type_no', lookup_expr='icontains', help_text='代码编号')
    type_name = django_filters.CharFilter(field_name='type_name', lookup_expr='icontains', help_text='代码名称')

    class Meta:
        model = GlobalCodeType
        fields = ('type_no', 'type_name')


class GlobalCodeFilter(django_filters.rest_framework.FilterSet):
    type_name = django_filters.CharFilter(field_name='global_type__type_name', help_text='全局代码类型名称')

    class Meta:
        model = GlobalCode
        fields = ('global_type_id', 'type_name')


class WorkAreaFilter(django_filters.rest_framework.FilterSet):
    area_ID = django_filters.CharFilter(field_name='area_ID', help_text='工作区ID', lookup_expr='icontains')
    area_name = django_filters.CharFilter(field_name='area_name', help_text='工作区名称', lookup_expr='icontains')
    rcs_address = django_filters.CharFilter(field_name='rcs_address', help_text='rcs地址', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', help_text='描述', lookup_expr='icontains')
    agv_type_name = django_filters.CharFilter(field_name='agv_type__type_name', lookup_expr='icontains')

    class Meta:
        model = WorkArea
        fields = ('id', 'area_ID', 'area_name', 'rcs_address', 'description', 'agv_type_name')


class ProcessSectionFilter(django_filters.rest_framework.FilterSet):
    process_ID = django_filters.CharFilter(field_name='process_ID', help_text='工艺段ID', lookup_expr='icontains')
    process_name = django_filters.CharFilter(field_name='process_name', help_text='工艺段名称', lookup_expr='icontains')
    source_process_name = django_filters.CharFilter(field_name='source_process__process_name', help_text='源工艺段名称', lookup_expr='icontains')
    target_process_name = django_filters.CharFilter(field_name='target_process__process_name', help_text='目标工艺段名称', lookup_expr='icontains')
    working_area_name = django_filters.CharFilter(field_name='working_area__area_name', help_text='工作区名称', lookup_expr='icontains')
    cell_numbers = django_filters.CharFilter(field_name='cell_numbers', help_text='单车电池片数量', lookup_expr='icontains')
    q_time = django_filters.CharFilter(field_name='q_time', help_text='物料超时时间', lookup_expr='icontains')
    pitch_time = django_filters.CharFilter(field_name='pitch_time', help_text='节拍', lookup_expr='icontains')
    upper_rail_type = django_filters.NumberFilter(field_name='upper_rail_type', help_text='上层轨道上下料类型')
    lower_rail_type = django_filters.NumberFilter(field_name='lower_rail_type', help_text='下层轨道上下料类型')
    upper_basket_type = django_filters.NumberFilter(field_name='upper_basket_type', help_text='上层花篮类型')
    lower_basket_type = django_filters.NumberFilter(field_name='lower_basket_type', help_text='下层花篮类型')
    ordered = django_filters.NumberFilter(field_name='ordering', help_text='顺序')

    class Meta:
        model = ProcessSection
        fields = ('id', 'process_ID', 'process_name', 'ordered', 'source_process', 'source_process_name', 'working_area_name',
                  'target_process', 'target_process_name', 'working_area', 'cell_numbers', 'q_time', 'pitch_time', 'upper_rail_type', 'lower_rail_type',
                  'upper_basket_type', 'lower_basket_type', 'warning_time', 'single_slot_num')


class PlatFormInfoFilter(django_filters.rest_framework.FilterSet):
    platform_ID = django_filters.CharFilter(field_name='platform_ID', help_text='站台ID', lookup_expr='icontains')
    platform_name = django_filters.CharFilter(field_name='platform_name', help_text='站台名称', lookup_expr='icontains')
    desc = django_filters.CharFilter(field_name='desc', help_text='描述', lookup_expr='icontains')
    working_area = django_filters.CharFilter(field_name='process__working_area', help_text='工作区')
    process_name = django_filters.CharFilter(field_name='process__process_name', help_text='所属工艺段', lookup_expr='icontains')
    q_time = django_filters.CharFilter(field_name='q_time', help_text='物料超时时间', lookup_expr='icontains')
    pitch_time = django_filters.CharFilter(field_name='pitch_time', help_text='节拍', lookup_expr='icontains')
    created_username = django_filters.CharFilter(field_name='created_user__username', help_text='创建人', lookup_expr='icontains')
    created_time = django_filters.DateFilter(field_name='created_time__date', help_text='创建时间')
    upper_rail_type = django_filters.NumberFilter(field_name='process__upper_rail_type', help_text='上层轨道上下料类型')
    lower_rail_type = django_filters.NumberFilter(field_name='process__lower_rail_type', help_text='下层轨道上下料类型')
    location_name = django_filters.CharFilter(field_name='location_name', help_text='位置名称', lookup_expr='icontains')
    platform_types = django_filters.CharFilter(method='filter_platform_types', help_text='所属定线')

    def filter_platform_types(self, queryset, name, value):
        platform_types = [int(i) for i in value.split(',')]
        return queryset.filter(platform_type__in=platform_types)

    class Meta:
        model = PlatFormInfo
        fields = ('id', 'platform_ID', 'platform_name', 'desc', 'process', 'working_area', 'is_used', 'process_name',
                  'q_time', 'pitch_time', 'created_username', 'created_time', 'upper_rail_type', 'lower_rail_type',
                  'location_name', 'platform_types')


class CacheDeviceInfoFilter(django_filters.rest_framework.FilterSet):
    device_ID = django_filters.CharFilter(field_name='device_ID', help_text='站台ID', lookup_expr='icontains')
    device_name = django_filters.CharFilter(field_name='device_name', help_text='站台名称', lookup_expr='icontains')
    desc = django_filters.CharFilter(field_name='desc', help_text='描述', lookup_expr='icontains')
    process = django_filters.ModelMultipleChoiceFilter(field_name='processes', help_text='工艺段',
                                                       queryset=ProcessSection.objects.all())
    in_location_name = django_filters.CharFilter(field_name='in_location_name', help_text='进料位置点名称', lookup_expr='icontains')
    out_location_name = django_filters.CharFilter(field_name='out_location_name', help_text='出料位置点名称', lookup_expr='icontains')
    working_area_name = django_filters.CharFilter(field_name='working_area__area_name', help_text='工作区名称', lookup_expr='icontains')
    allow_task_num = django_filters.NumberFilter(field_name='allow_task_num', help_text='允许任务数')
    created_username = django_filters.CharFilter(field_name='created_user__username', help_text='创建人', lookup_expr='icontains')
    created_time = django_filters.DateFilter(field_name='created_time__date', help_text='创建时间')
    route_schemas = django_filters.CharFilter(method='filter_route_schemas', help_text='所属定线')

    def filter_route_schemas(self, queryset, name, value):
        relates = CacheDeviceRouteRelation.objects.filter(group__route_schema__route_name__icontains=value).values_list('cache_device_id', flat=True)
        return queryset.filter(id__in=relates)

    class Meta:
        model = CacheDeviceInfo
        fields = ('id', 'device_ID', 'device_name', 'desc', 'working_area', 'in_is_used', 'out_is_used',
                  'process', 'in_location_name', 'out_location_name', 'working_area_name',
                  'allow_task_num', 'created_username', 'created_time', 'route_schemas', 'task_priority')


class RestLocationFilter(django_filters.rest_framework.FilterSet):
    location_ID = django_filters.CharFilter(field_name='location_ID', help_text='位置ID', lookup_expr='icontains')
    location_name = django_filters.CharFilter(field_name='location_name', help_text='位置点名称', lookup_expr='icontains')
    desc = django_filters.CharFilter(field_name='desc', help_text='描述', lookup_expr='icontains')
    working_area = django_filters.CharFilter(field_name='working_area', help_text='工作区')
    working_area_name = django_filters.CharFilter(field_name='working_area__area_name', help_text='工作区名称', lookup_expr='icontains')
    processes = django_filters.ModelMultipleChoiceFilter(field_name='processes', help_text='工艺段', queryset=ProcessSection.objects.all())
    created_username = django_filters.CharFilter(field_name='created_user__username', help_text='创建人', lookup_expr='icontains')
    created_time = django_filters.DateFilter(field_name='created_time__date', help_text='创建时间')
    route_str = django_filters.CharFilter(method='filter_route_str', help_text='所属定线')

    def filter_route_str(self, queryset, name, value):
        relates = RestLocationRouteRelation.objects.filter(group__route_schema__route_name__icontains=value).values_list('rest_location_id', flat=True)
        return queryset.filter(id__in=relates)

    class Meta:
        model = RestLocation
        fields = ('id', 'location_ID', 'location_name', 'desc', 'working_area', 'processes', 'working_area_name', 'created_username',
                  'created_time', 'route_str', 'is_used')


class LocationFilter(django_filters.rest_framework.FilterSet):
    location_name = django_filters.CharFilter(field_name='location_name', help_text='位置点名称', lookup_expr='icontains')
    created_username = django_filters.CharFilter(field_name='created_user__username', help_text='创建人', lookup_expr='icontains')
    created_time = django_filters.DateFilter(field_name='created_time__date', help_text='创建时间')
    last_updated_username = django_filters.CharFilter(field_name='last_updated_user__username', help_text='修改人',
                                                      lookup_expr='icontains')
    last_updated_time = django_filters.DateFilter(field_name='last_updated_time__date', help_text='修改时间')

    class Meta:
        model = Location
        fields = ('location_name', 'created_username', 'created_time', 'last_updated_username',
                  'last_updated_time', 'is_used')


class LocationGroupFilter(django_filters.rest_framework.FilterSet):
    group_code = django_filters.CharFilter(field_name='group_code', help_text='休息位组编号', lookup_expr='icontains')
    group_name = django_filters.CharFilter(field_name='group_name', help_text='休息位组名称', lookup_expr='icontains')
    created_username = django_filters.CharFilter(field_name='created_user__username', help_text='创建人', lookup_expr='icontains')
    created_time = django_filters.DateFilter(field_name='created_time__date', help_text='创建时间')
    last_updated_username = django_filters.CharFilter(field_name='last_updated_user__username', help_text='修改人',
                                                      lookup_expr='icontains')
    last_updated_time = django_filters.DateFilter(field_name='last_updated_time__date', help_text='修改时间')
    location_names = django_filters.CharFilter(method='filter_contain_location', help_text='所选休息位')

    def filter_contain_location(self, queryset, name, value):
        relates = LocationGroupRelation.objects.filter(location__location_name__icontains=value).values_list('location_group_id', flat=True)
        return queryset.filter(id__in=relates)

    class Meta:
        model = LocationGroup
        fields = ('group_code', 'group_name', 'created_username', 'created_time',
                  'last_updated_username', 'last_updated_time', 'location_names')


class PlatformGroupFilter(django_filters.rest_framework.FilterSet):
    group_name = django_filters.CharFilter(field_name='group_name', help_text='设备组名称', lookup_expr='icontains')

    class Meta:
        model = PlatformGroup
        fields = ('route_schema', 'group_ID', 'group_name', 'group_type', 'process', 'maximum', 'minimum',
                  'warning_maximum', 'warning_minimum')

#
# class PlatFormInfoOrderingFilter(OrderingFilter):
#     def remove_invalid_fields(self, queryset, fields, view, request):
#         valid_fields = [field.lstrip('-') for field in fields]
#         renamed_fields = []
#         for field in valid_fields:
#             if field == 'process_name':
#                 renamed_fields.append('process__process_name')
#             elif field == 'working_area_name':
#                 renamed_fields.append('process__working_area__area_name')
#             elif field == 'upper_rail_type':
#                 renamed_fields.append('process__upper_rail_type')
#             elif field == 'lower_rail_type':
#                 renamed_fields.append('process__lower_rail_type')
#             elif field == 'created_username':
#                 renamed_fields.append('created_user__username')
#             else:
#                 renamed_fields.append(field)
#         return super().remove_invalid_fields(queryset, renamed_fields, view, request)


class PlatFormInfoOrderingFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering:
            mapping = {
                'process_name': 'process__process_name',
                'working_area_name': 'process__working_area__area_name',
                'upper_rail_type': 'process__upper_rail_type',
                'lower_rail_type': 'process__lower_rail_type',
                'created_username': 'created_user__username',
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


class RestLocationOrderingFilter(OrderingFilter):

    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering:
            mapping = {
                'created_username': 'created_user__username',
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


class LocationOrderingFilter(OrderingFilter):

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


class CacheDeviceInfoOrderingFilter(OrderingFilter):

    def get_ordering(self, request, queryset, view):
        ordering = super().get_ordering(request, queryset, view)
        if ordering:
            mapping = {
                'created_username': 'created_user__username',
                'working_area_name': 'working_area__area_name',
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


class ThresholdDisplayFilter(django_filters.rest_framework.FilterSet):
    platform_ID = django_filters.CharFilter(field_name='platform_ID', lookup_expr='icontains', help_text='设备编号')
    platform_name = django_filters.CharFilter(field_name='platform_name', lookup_expr='icontains', help_text='设备名称')
    group_name = django_filters.CharFilter(field_name='group__group_name', lookup_expr='icontains', help_text='本线设备')
    shunt_platform_group_name = django_filters.ModelMultipleChoiceFilter(field_name='shunt_platform_group', queryset=PlatformGroup.objects.all(), help_text='分流来源设备')

    class Meta:
        model = PlatFormInfo
        fields = ('platform_ID', 'platform_name', 'group_name', 'shunt_platform_group_name')
