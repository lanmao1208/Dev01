from rest_framework import serializers
from rest_framework import validators

from .models import Configures
from projects.models import Projects
from utils.common import datetime_fmt


class ConfiguresModelSerializer(serializers.ModelSerializer):
    # project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    # project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
    #                                                 queryset=Projects.objects.all(), write_only=True)

    class Meta:
        model = Configures
        fields = ('id', 'name', 'project', 'project_id', 'include', 'create_time', 'update_time')

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': datetime_fmt()
            },
            'update_time': {
                'read_only': True,
                'format': datetime_fmt()
            },
            'include': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            return super().update(instance, validated_data)