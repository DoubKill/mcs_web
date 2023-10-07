from django.db.transaction import atomic
from rest_framework import serializers

from agv.models import Tasks, EnvCheckLocations, EnvCheckTasks, EnvTaskLocationRelation, EnvLocationCheckHistory
from basics.serializers import BaseModelSerializer
from mcs.settings import COMMON_READ_ONLY_FIELDS


class EquipTaskTrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = ('id', 'platform_name', 'agv_no', 'process_name', 'end_time', 'receive_time', 'origin_platform_name')


class EnvCheckLocationsSerializer(BaseModelSerializer):
    working_area_name = serializers.ReadOnlyField(source='working_area.area_name')

    class Meta:
        model = EnvCheckLocations
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class EnvTaskLocationRelationSerializer(serializers.ModelSerializer):
    location_name = serializers.ReadOnlyField(source='check_location.location_name')

    class Meta:
        model = EnvTaskLocationRelation
        fields = ('check_location', 'ordering', 'location_name')


class EnvCheckTasksSerializer(serializers.ModelSerializer):
    working_area_name = serializers.ReadOnlyField(source='working_area.area_name')
    envtasklocationrelation_set = EnvTaskLocationRelationSerializer(many=True)

    def to_representation(self, instance):
        ret = super(EnvCheckTasksSerializer, self).to_representation(instance)
        env_relts = ret['envtasklocationrelation_set']
        sorted_env_relts = sorted(env_relts, key=lambda x: x['ordering'])
        ret['envtasklocationrelation_set'] = sorted_env_relts
        return ret

    @atomic()
    def create(self, validated_data):
        lcs = validated_data.pop('envtasklocationrelation_set')
        instance = super().create(validated_data)
        for item in lcs:
            EnvTaskLocationRelation.objects.create(
                check_location=item['check_location'],
                ordering=item['ordering'],
                check_task=instance
            )
        return instance

    @atomic()
    def update(self, instance, validated_data):
        lcs = validated_data.pop('envtasklocationrelation_set')
        instance = super().update(instance, validated_data)
        instance.locations.clear()
        for item in lcs:
            EnvTaskLocationRelation.objects.create(
                check_location=item['check_location'],
                ordering=item['ordering'],
                check_task=instance
            )
        return instance

    class Meta:
        model = EnvCheckTasks
        fields = '__all__'
        read_only_fields = COMMON_READ_ONLY_FIELDS


class EnvLocationCheckHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EnvLocationCheckHistory
        fields = '__all__'