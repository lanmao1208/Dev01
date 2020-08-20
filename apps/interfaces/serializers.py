from rest_framework import serializers, validators
from .models import Interfaces
from configures.models import Configures
from projects.models import Projects
from testcases.serializers import TestcasesModelSerializer
# from configures.serializers import ConfiguresModelSerializer
from utils import common


# 使用模型序列化器类：简化序列化器类中字段的创建
class InterfacesModelSerializer(serializers.ModelSerializer):
    # 因为project为外键字段，所以此地使用project or project_id都行
    project = serializers.StringRelatedField(help_text='所属项目名称', label='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(write_only=True, help_text='所属项目ID', label='所属项目ID',
                                                    queryset=Projects.objects.all())

    # project_id = serializers.IntegerField(write_only=True, validators=[])

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'tester', 'project', 'create_time', 'project_id', 'desc')
        extra_kwargs = {
            "create_time": {
                'read_only': True,
                'format': common.datetime_fmt()
            },
            "name": {
                "validators": [validators.UniqueValidator(queryset=model.objects.all(), message='项目名称不能重复')]
            }
        }

    def create(self, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
            return super().update(instance, validated_data)


class TestcasesByInterfacesIdModelSerializer(serializers.ModelSerializer):
    testcases = TestcasesModelSerializer(label='用例信息', help_text='用例信息', many=True)

    class Meta:
        model = Interfaces
        fields = ("testcases",)


class ConfiguresNamesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configures
        fields = ('id', 'name')


class ConfiguresByInterfacesIdModelSerializer(serializers.ModelSerializer):
    configuers = ConfiguresNamesModelSerializer(label='配置信息', help_text='配置信息', many=True)

    class Meta:
        model = Interfaces
        fields = ("configuers",)
