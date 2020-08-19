from rest_framework import serializers
from rest_framework import validators

from testcases.models import Testcases
from interfaces.models import Interfaces
from DEV01 import validaters
from projects.models import Projects
from utils.common import datetime_fmt


class InterfacesProjectsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    Pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True,
                                   validators=[validaters.projects_id_bool])
    Iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True,
                                   validators=[validaters.interfaces_id_bool])

    class Meta:
        model = Interfaces
        field = ("name", "Pid", "Iid")

    def validate(self, attrs):
        Pid = attrs.get("Pid")
        Iid = attrs.get("Iid")
        # 效验接口id和项目id是否匹配
        if not Interfaces.objects.filter(id=Iid, project_id=Pid).exists():
            raise serializers.ValidationError("接口id和项目id并未匹配")


class TestcasesModelSerializer(serializers.ModelSerializer):
    interfaces = InterfacesProjectsModelSerializer(label='所属项目和接口', help_text='所属项目和接口')

    class Meta:
        model = Testcases
        exclude = ('create_time', 'update_time')

        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        Iid = validated_data.pop("interfaces").get("Iid")
        validated_data["interfaces_id"] = Iid
        return super().create(validated_data)

    def update(self, instance, validated_data):
        Iid = validated_data.pop("interfaces").get("Iid")
        Pid = validated_data.pop("projects").get("Pid")
        validated_data["interfaces_id"] = Iid
        validated_data["projects_id"] = Pid
        return super().update(instance,validated_data)