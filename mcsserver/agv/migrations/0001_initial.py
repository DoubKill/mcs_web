# Generated by Django 3.1 on 2023-07-22 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CacheDeviceStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equip_code', models.CharField(help_text='缓存设备编号', max_length=128, verbose_name='缓存设备编号')),
                ('row', models.PositiveIntegerField(help_text='排', verbose_name='排')),
                ('column', models.PositiveIntegerField(help_text='列', verbose_name='列')),
                ('layer', models.PositiveIntegerField(help_text='层', verbose_name='层')),
                ('in_processID', models.CharField(blank=True, help_text='入库工艺段ID', max_length=256, null=True, verbose_name='入库工艺段ID')),
                ('in_material_type_name', models.CharField(blank=True, help_text='入库物料类型', max_length=128, null=True, verbose_name='入库物料类型')),
                ('equipID', models.CharField(blank=True, help_text='来源站台ID', max_length=128, null=True, verbose_name='来源站台ID')),
                ('output_time_consume', models.IntegerField(blank=True, help_text='下料到入库耗时', null=True, verbose_name='下料到入库耗时')),
                ('q_time', models.IntegerField(blank=True, help_text='物料超时时间(秒)', null=True, verbose_name='物料超时时间(秒)')),
                ('in_task_no', models.CharField(blank=True, help_text='入库任务号', max_length=128, null=True, verbose_name='入库任务号')),
                ('basket_num', models.IntegerField(default=0, help_text='库位花篮数', verbose_name='库位花篮数')),
            ],
            options={
                'verbose_name': '缓存堆栈库存信息',
                'verbose_name_plural': '缓存堆栈库存信息',
                'db_table': 'dam_cache_device_stock',
            },
        ),
        migrations.CreateModel(
            name='RCSCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_no', models.CharField(help_text='任务号', max_length=128, verbose_name='任务号')),
                ('command_type', models.PositiveIntegerField(choices=[(1, '取消订单'), (2, '变更终点'), (3, '强制完成')], help_text='操作类型', verbose_name='操作类型')),
                ('current_retry_times', models.PositiveIntegerField(default=0, help_text='当前重试次数', verbose_name='当前重试次数')),
                ('last_retry_time', models.DateTimeField(blank=True, help_text='上次重试时间', null=True, verbose_name='上次重试时间')),
                ('error_reason', models.CharField(blank=True, help_text='失败原因', max_length=2048, null=True, verbose_name='失败原因')),
                ('created_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('last_updated_time', models.DateTimeField(auto_now=True, help_text='修改时间', verbose_name='修改时间')),
                ('send_data', models.JSONField(blank=True, help_text='发送数据', null=True, verbose_name='发送数据')),
            ],
            options={
                'verbose_name': 'RCS订单操作',
                'verbose_name_plural': 'RCS订单操作',
                'db_table': 'dma_tasks_command',
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_no', models.CharField(help_text='任务号', max_length=128, verbose_name='任务号')),
                ('task_type', models.PositiveIntegerField(choices=[(1, '导航'), (2, '取货'), (3, '卸货'), (4, '取卸货')], help_text='任务类型', verbose_name='任务类型')),
                ('agv_no', models.IntegerField(blank=True, help_text='AGV车号', null=True, verbose_name='AGV车号')),
                ('end_location', models.CharField(help_text='站台位置点', max_length=128, verbose_name='站台位置点')),
                ('platform_ID', models.CharField(blank=True, help_text='站台ID', max_length=256, null=True, verbose_name='站台ID')),
                ('platform_name', models.CharField(blank=True, help_text='站台名称', max_length=256, null=True, verbose_name='站台名称')),
                ('route_name', models.CharField(blank=True, help_text='定线名称', max_length=256, null=True, verbose_name='定线名称')),
                ('priority', models.PositiveIntegerField(blank=True, help_text='优先级', null=True, verbose_name='优先级')),
                ('state', models.PositiveIntegerField(choices=[(1, '已创建'), (2, '待下发'), (3, '已下发'), (4, '已派车'), (5, '已到达'), (6, '开始对接'), (7, '完成'), (8, '失败'), (9, '已取消')], help_text='任务执行状态', verbose_name='任务执行状态')),
                ('error_reason', models.CharField(blank=True, help_text='状态说明', max_length=2048, null=True, verbose_name='状态说明')),
                ('created_time', models.DateTimeField(auto_now_add=True, help_text='任务创建时间', verbose_name='任务创建时间')),
                ('last_updated_time', models.DateTimeField(auto_now=True, help_text='任务修改时间', verbose_name='任务修改时间')),
                ('axis1_action', models.PositiveIntegerField(blank=True, choices=[(0, ''), (1, '取货'), (2, '卸货')], help_text='AGV轴1动作类型', null=True, verbose_name='AGV轴1动作类型')),
                ('axis2_action', models.PositiveIntegerField(blank=True, choices=[(0, ''), (1, '取货'), (2, '卸货')], help_text='AGV轴2动作类型', null=True, verbose_name='AGV轴2动作类型')),
                ('axis3_action', models.PositiveIntegerField(blank=True, choices=[(0, ''), (1, '取货'), (2, '卸货')], help_text='AGV轴3动作类型', null=True, verbose_name='AGV轴3动作类型')),
                ('axis4_action', models.PositiveIntegerField(blank=True, choices=[(0, ''), (1, '取货'), (2, '卸货')], help_text='轴4动作类型', null=True, verbose_name='轴4动作类型')),
                ('axis1_package_name', models.CharField(blank=True, help_text='AGV轴1包号', max_length=128, null=True, verbose_name='AGV轴1包号')),
                ('axis2_package_name', models.CharField(blank=True, help_text='AGV轴2包号', max_length=128, null=True, verbose_name='AGV轴2包号')),
                ('axis3_package_name', models.CharField(blank=True, help_text='AGV轴3包号', max_length=128, null=True, verbose_name='AGV轴3包号')),
                ('axis4_package_name', models.CharField(blank=True, help_text='AGV轴4包号', max_length=128, null=True, verbose_name='AGV轴4包号')),
                ('rcs_order_id', models.BigIntegerField(blank=True, help_text='rcs订单ID', null=True, verbose_name='rcs订单ID')),
                ('change_time', models.DateTimeField(blank=True, help_text='任务变更时间', null=True, verbose_name='任务变更时间')),
                ('active_time', models.DateTimeField(blank=True, help_text='RCS激活订单时间', null=True, verbose_name='RCS激活订单时间')),
                ('dispatched_time', models.DateTimeField(blank=True, help_text='RCS调度时间', null=True, verbose_name='RCS派车时间')),
                ('bind_time', models.DateTimeField(blank=True, help_text='RCS派车时间', null=True, verbose_name='RCS派车时间')),
                ('begin_time', models.DateTimeField(blank=True, help_text='AGV开始开始时间', null=True, verbose_name='AGV开始开始时间')),
                ('arrived_time', models.DateTimeField(blank=True, help_text='AGV到达时间', null=True, verbose_name='小车到达时间')),
                ('begin_act_time', models.DateTimeField(blank=True, help_text='开始对接时间', null=True, verbose_name='开始对接时间')),
                ('end_time', models.DateTimeField(blank=True, help_text='完成时间', null=True, verbose_name='完成时间')),
                ('error_time', models.DateTimeField(blank=True, help_text='error时间', null=True, verbose_name='error时间')),
            ],
            options={
                'verbose_name': 'MCS任务表',
                'verbose_name_plural': 'MCS任务表',
                'db_table': 'dma_tasks',
            },
        ),
        migrations.AddIndex(
            model_name='tasks',
            index=models.Index(fields=['agv_no'], name='dma_tasks_agv_no_b61fe2_idx'),
        ),
        migrations.AddIndex(
            model_name='tasks',
            index=models.Index(fields=['state'], name='dma_tasks_state_591c2d_idx'),
        ),
        migrations.AddIndex(
            model_name='tasks',
            index=models.Index(fields=['task_type'], name='dma_tasks_task_ty_5a83f5_idx'),
        ),
        migrations.AddIndex(
            model_name='tasks',
            index=models.Index(fields=['platform_ID'], name='dma_tasks_platfor_a81896_idx'),
        ),
        migrations.AddField(
            model_name='rcscommand',
            name='task',
            field=models.ForeignKey(help_text='MCS任务', on_delete=django.db.models.deletion.CASCADE, to='agv.tasks', verbose_name='MCS任务'),
        ),
    ]