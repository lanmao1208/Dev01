from rest_framework import serializers
from rest_framework import validators

from .models import DebugTalks
from utils import common


class DebugTalksModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text="所属项目名称", label="所属项目名称")

    class Meta:
        model = DebugTalks
        exclude = ('create_time', 'update_time')
        read_only_fields = ('name', 'project')

        extra_kwargs = {
            'debugtalk': {
                'write_only': True,
            }
        }



