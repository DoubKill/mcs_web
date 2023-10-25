# coding: utf-8
"""项目初始化脚本"""
import json
import os

import django
import shutil


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcs.settings")
django.setup()

from user.models import User, Permissions, Department
from basics.models import Configuration

method_dict = {
    'view': '查看',
    'add': '新增',
    'change': '修改',
    'update': '启用/停用',
    'delete': '删除',
    'import': '导入',
    'export': '导出',
}


ps_data = [
    {
        'code': 'users',
        'name': '用户管理',
        'category_name': '系统管理',
        'operations': ['view', 'add', 'change', 'update', 'delete']
    },
    {
        'code': 'roles',
        'name': '角色管理',
        'category_name': '系统管理',
        'operations': ['view', 'add', 'change', 'delete']
    },
    {
        'code': 'department',
        'name': '人员组织架构',
        'category_name': '系统管理',
        'operations': ['view', 'add', 'change', 'delete']
    },
    {
        'code': 'operation_log',
        'name': '操作履历',
        'category_name': '系统管理',
        'operations': ['view']
    },
    {
        'code': 'global_conf',
        'name': '全局配置',
        'category_name': '基础信息管理',
        'operations': ['view', 'change']
    },
    {
        'code': 'agv_type',
        'name': 'AGV类型管理',
        'category_name': '基础信息管理',
        'operations': ['view', 'add', 'change', 'delete']
    },
    {
        'code': 'work_area',
        'name': '工作区管理',
        'category_name': '基础信息管理',
        'operations': ['view', 'add', 'change', 'delete']
    },
    {
        'code': 'process',
        'name': '工艺段配置',
        'category_name': '基础信息管理',
        'operations': ['view', 'add', 'change', 'delete', 'export']
    },
    {
        'code': 'locations',
        'name': '休息位管理',
        'category_name': '基础信息管理',
        'operations': ['view', 'add', 'change', 'delete', 'update']
    },
    {
        'code': 'location_groups',
        'name': '休息位组管理',
        'category_name': '基础信息管理',
        'operations': ['view', 'add', 'change', 'delete']
    },
    {
        'code': 'stations',
        'name': '工艺站台管理',
        'category_name': '基础信息管理',
        'operations': ['view', 'add', 'change', 'delete', 'update', 'import', 'export']
    },
    {
        'code': 'caches',
        'name': '堆栈站台管理',
        'category_name': '基础信息管理',
        'operations': ['view', 'add', 'change', 'delete', 'update']
    },
    {
        'code': 'check_conf',
        'name': '配置检查',
        'category_name': '基础信息管理',
        'operations': ['view']
    },
    {
        'code': 'schemas',
        'name': '定线管理',
        'category_name': '设置定线',
        'operations': ['view', 'add', 'change']
    },
    {
        'code': 'empty_schemas',
        'name': '空花篮定线',
        'category_name': '设置定线',
        'operations': ['view', 'change']
    },
    {
        'code': 'dev_groups',
        'name': '设备组设置',
        'category_name': '设置定线',
        'operations': ['view', 'change']
    },
    {
        'code': 'tasks',
        'name': '任务监控',
        'category_name': '设备监控',
        'operations': ['view', 'change']
    },
    {
        'code': 'agv_state',
        'name': 'AGV状态监控',
        'category_name': '设备监控',
        'operations': ['view']
    },
    {
        'code': 'agv_package',
        'name': 'AGV物料监控',
        'category_name': '设备监控',
        'operations': ['view']
    },
    {
        'code': 'station_state',
        'name': '站台状态监控',
        'category_name': '设备监控',
        'operations': ['view']
    },
    {
        'code': 'cache_state',
        'name': '堆栈状态监控',
        'category_name': '设备监控',
        'operations': ['view']
    },
    {
        'code': 'real_state',
        'name': '站台实时监控',
        'category_name': '设备监控',
        'operations': ['view']
    },
    {
        'code': 'zz_state',
        'name': '在制产能汇总',
        'category_name': '设备监控',
        'operations': ['view']
    },
    {
        'code': 'history_tasks',
        'name': '历史任务查询',
        'category_name': '报表数据',
        'operations': ['view', 'export']
    },
    {
        'code': 'product_static',
        'name': '工序产能报表',
        'category_name': '报表数据',
        'operations': ['view', 'export']
    },
    {
        'code': 'equip_static',
        'name': '机台产能报表',
        'category_name': '报表数据',
        'operations': ['view', 'export']
    },
    {
        'code': 'threshold_display',
        'name': '分流展示',
        'category_name': '报表数据',
        'operations': ['view']
    },
    {
        'code': 'agv_in_process',
        'name': 'AGV实时在制',
        'category_name': '报表数据',
        'operations': ['view']
    },
    {
        'code': 'in_process_trend',
        'name': '在制趋势',
        'category_name': '报表数据',
        'operations': ['view']
    },
    {
        'code': 'alarm',
        'name': '告警记录',
        'category_name': '告警记录',
        'operations': ['view']
    },
    {
        'code': 'qtime_report',
        'name': '堆栈超时料报表',
        'category_name': '报表数据',
        'operations': ['view']
    },
    {
        'code': 'station_track',
        'name': '站台任务追溯报表',
        'category_name': '报表数据',
        'operations': ['view']
    },
    {
        'code': 'task_duration_report',
        'name': '任务时长统计报表',
        'category_name': '报表数据',
        'operations': ['view']
    },
    # {
    #     'code': 'env_indicator',
    #     'name': '检测指标阈值设置',
    #     'category_name': '环境检测',
    #     'operations': ['view', 'change']
    # },
    # {
    #     'code': 'env_location',
    #     'name': '检测点配置',
    #     'category_name': '环境检测',
    #     'operations': ['view', 'add', 'change', 'delete']
    # },
    # {
    #     'code': 'env_task',
    #     'name': '检测任务配置',
    #     'category_name': '环境检测',
    #     'operations': ['view', 'add', 'change', 'delete']
    # },
    # {
    #     'code': 'env_check_history',
    #     'name': '检测报表',
    #     'category_name': '环境检测',
    #     'operations': ['view', 'export']
    # },
]


def init_permissions():
    for item in ps_data:
        pm_code = item['code']
        child_perms = item.pop('operations', [])
        pp = Permissions.objects.create(**item)
        for c in child_perms:
            cp_data = {'code': '{}_{}'.format(c, pm_code), 'name': method_dict[c], 'parent': pp}
            Permissions.objects.create(**cp_data)


global_conf_data = [
        {'key': 'zz_sum_type', 'desc': '在制统计方式', 'value_type': 'choices', 'choices': {'1': '带料AGV', '2': '带料空闲AGV', '3': '上游+下游+带料AGV'}, 'value': '1'},
        {'key': 'transfer_time', 'desc': '传篮时间(秒)', 'value_type': 'int', 'value': '15'},
        {'key': 'agv_mixture_material_flag', 'desc': '是否允许混接', 'value_type': 'bool', 'value': '0'},
        {'key': 'wcs_url', 'desc': 'WCS地址(ip:port)', 'value_type': 'str', 'value': 'http://127.0.0.1:9999'},
        {'key': 'rcs_url', 'desc': 'RCS地址(ip:port)', 'value_type': 'str', 'value': 'http://127.0.0.1:2000'},
        {'key': 'task_switch', 'desc': '调度任务开关', 'value_type': 'choices', 'choices': {'1': '开启', '2': '关闭'}, 'value': '1'},
        {'key': 'stack_task_eta', 'desc': '堆栈任务AGV ETA（秒）', 'value_type': 'int', 'value': '300'},
        {'key': 'shift_time', 'desc': '倒班时间规则', 'value_type': 'json_date', 'value': '{"早班":"08:00:00-20:00:00","晚班":"20:00:00-08:00:00"}'},
        {'key': 'resend_task', 'desc': '是否重新下发任务', 'value_type': 'bool', 'value': '1'},
        {'key': 'env_valid_time', 'desc': '环境检测失效时间(分)', 'value_type': 'int', 'value': '30'},
    ]


def init_global_conf():
    for item in global_conf_data:
        Configuration.objects.create(**item)


def main():
    print('开始迁移数据库')
    # apps = ('agv', 'basics', 'monitor', 'openapi', 'user')
    #
    # for app in apps:
    #     try:
    #         shutil.rmtree(f"{app}/migrations")
    #     except Exception:
    #         pass
    #
    # os.system(
    #     'python manage.py makemigrations {}'.format(
    #         ' '.join(apps)
    #     ))
    os.system('python manage.py migrate')
    os.system('python manage.py collectstatic --noinput')

    print('创建超级管理员...')
    User.objects.create_superuser('gzmcs123', '123456@qq.com', '123456')
    Department.objects.create(name='浙江国自机器人技术股份有限公司')
    init_permissions()
    init_global_conf()


if __name__ == '__main__':
    main()
