from rest_framework import serializers

from agv.models import Tasks
from monitor.models import AlarmLog


# from monitor.models import BasketTransportMonitor


# class BasketTransportMonitorSerializer(serializers.ModelSerializer):
#     process_name = serializers.ReadOnlyField(source='platform.equip.process.process_name')
#     equip_name = serializers.ReadOnlyField(source='platform.equip.equip_name')
#     platform_name = serializers.ReadOnlyField(source='platform.platform_name')
#
#     class Meta:
#         model = BasketTransportMonitor
#         fields = '__all__'


class TaskMonitorSerializer(serializers.ModelSerializer):
    axis1_action_name = serializers.ReadOnlyField(source='get_axis1_action_display')
    axis2_action_name = serializers.ReadOnlyField(source='get_axis2_action_display')
    axis3_action_name = serializers.ReadOnlyField(source='get_axis3_action_display')
    axis4_action_name = serializers.ReadOnlyField(source='get_axis4_action_display')
    task_type_name = serializers.ReadOnlyField(source='get_task_type_display')
    state_name = serializers.ReadOnlyField(source='get_state_display')

    class Meta:
        model = Tasks
        fields = '__all__'


class TaskHistorySerializer(serializers.ModelSerializer):
    task_type_name = serializers.ReadOnlyField(source='get_task_type_display')
    state_name = serializers.ReadOnlyField(source='get_state_display')
    task_time_consume = serializers.SerializerMethodField()
    task_move_consume = serializers.SerializerMethodField()
    task_interact_consume = serializers.SerializerMethodField()

    def get_task_time_consume(self, obj):
        try:
            return int((obj.end_time - obj.created_time).total_seconds())
        except Exception:
            return ''

    def get_task_move_consume(self, obj):
        try:
            return int((obj.arrived_time - obj.bind_time).total_seconds())
        except Exception:
            return ''

    def get_task_interact_consume(self, obj):
        try:
            return int((obj.end_time - obj.begin_act_time).total_seconds())
        except Exception:
            return ''

    class Meta:
        model = Tasks
        fields = ('task_no', 'platform_ID', 'platform_name', 'end_location', 'agv_no', 'state_name', 'task_type_name',
                  'origin_platform_name', 'created_time', 'arrived_time', 'end_time',
                  'task_time_consume', 'task_move_consume', 'task_interact_consume')


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmLog
        fields = '__all__'
