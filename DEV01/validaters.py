from rest_framework import serializers

from projects.models import Projects
from interfaces.models import Interfaces


def project_id_bool(value):
    # 效验项目id是否存在
    if not Projects.objects.filter(id=value).exists():
        raise serializers.ValidationError("项目id不存在")


def interface_id_bool(value):
    # 效验接口id是否存在
    if not Interfaces.objects.filter(id=value).exists():
        raise serializers.ValidationError("接口id不存在")