import django_filters

from user.models import User, Department, GroupExtension, UserOperationLog


class UserFilter(django_filters.rest_framework.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains', help_text='用户名')
    groups = django_filters.CharFilter(field_name='group_extensions', help_text='角色id')
    department_name = django_filters.CharFilter(field_name='department__name', lookup_expr='icontains', help_text='部门')
    created_username = django_filters.CharFilter(field_name='created_user__username', lookup_expr='icontains', help_text='创建人')
    last_update_username = django_filters.CharFilter(field_name='last_updated_user__username', lookup_expr='icontains', help_text='修改人')
    created_time = django_filters.DateFilter(field_name='created_time__date', help_text='创建日期')
    last_updated_time = django_filters.DateFilter(field_name='last_updated_time__date', help_text='修改日期')

    class Meta:
        model = User
        fields = ('username', 'groups', 'is_active', 'department_name', 'is_superuser', 'created_username', 'created_time', 'last_update_username',
                  'last_updated_time')


class GroupExtensionFilter(django_filters.rest_framework.FilterSet):
    group_code = django_filters.CharFilter(field_name="group_code", lookup_expr="icontains", help_text="角色代码")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains", help_text="角色名称")
    created_user = django_filters.CharFilter(field_name="created_user__username", lookup_expr="icontains", help_text="创建人")
    created_time = django_filters.DateFilter(field_name='created_time__date', help_text='创建日期')

    class Meta:
        model = GroupExtension
        fields = {"group_code", "name", 'is_used', 'created_user', 'created_time'}


class DepartmentFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', help_text='名称', lookup_expr='icontains')
    department_id = django_filters.CharFilter(field_name='department_id', help_text="编码", lookup_expr='icontains')

    class Meta:
        model = Department
        fields = ('name', 'parent_section_id')


class UserOperationLogFilter(django_filters.rest_framework.FilterSet):
    operator_user = django_filters.CharFilter(field_name='operator_user', help_text='操作人', lookup_expr='icontains')
    operator_date = django_filters.DateFromToRangeFilter(field_name='create_time__date', help_text='操作日期', lookup_expr='range')
    operator_time = django_filters.DateFilter(field_name='create_time__date', help_text='操作时间')
    operation_desc = django_filters.CharFilter(field_name='operation_desc', help_text='操作描述', lookup_expr='icontains')
    operator_reason = django_filters.CharFilter(field_name='operator_reason', help_text='操作原因', lookup_expr='icontains')
    operator_type = django_filters.CharFilter(field_name='operator_type', help_text='操作类型', lookup_expr='icontains')

    class Meta:
        model = UserOperationLog
        fields = ('operator_user', 'operator_date', 'operator_time', 'operation_desc', 'operator_reason', 'operator_type')

