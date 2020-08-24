from rest_framework import serializers
from rest_framework import validators

from .models import Configures
from projects.models import Projects
from interfaces.models import Interfaces
from utils import validates


class InterfacesProjectsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True,
                                   validators=[validates.is_exised_project_id])
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True,
                                   validators=[validates.is_exised_interface_id()])

    class Meta:
        model = Interfaces
        fields = ("name", "pid", "Iid", "project")

    def validate(self, attrs):
        pid = attrs.get("pid")
        iid = attrs.get("iid")
        # 效验接口id和项目id是否匹配
        if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError("接口id和项目id并未匹配")


class ConfiguresModelSerializer(serializers.ModelSerializer):
    interface = InterfacesProjectsModelSerializer(label='所属项目和接口', help_text='所属项目和接口')

    class Meta:
        model = Configures
        exclude = ('create_time', 'update_time')
        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }

        def create(self, validated_data):
            iid = validated_data.pop("interface").get("iid")
            validated_data["interface_id"] = iid
            return super().create(validated_data)

        def update(self, instance, validated_data):
            iid = validated_data.pop("interface").get("iid")
            validated_data["interface_id"] = iid
            return super().update(instance, validated_data)
