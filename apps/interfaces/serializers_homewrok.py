from rest_framework import serializers
from rest_framework import validators
from .models import Interfaces


# 定义筛选条件类
# value为前端输入待效验的值
def is_name_contain_x(value):
    if "x" in value:
        # 不符合效验条件，必须抛出ValidationError该异常，不可变
        raise serializers.ValidationError("项目名称中不能包含x")


# ModelSerializer方法
class InterfacesModelSerializer(serializers.ModelSerializer):
    projects = serializers.StringRelatedField()

    creat_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    updata_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    class Meta:

        model = Interfaces
        fields = '__all__'
        extra_kwargs = {
            "tester": {
                'label': '研发人员',
                'write_only': True,
                'max_length': 20,
                'min_length': 2
            },
            "name": {
                'max_length': 20,
                'min_length': 2,
                'validators': [is_name_contain_x]
            }
        }

    def validate_name(self, value):
        if "x" in value:
            raise serializers.ValidationError("项目名称中不能包含x")

        return value

    def validate(self, attrs):
        if len(attrs["name"]) != 8 or "测试" not in attrs:
            raise serializers.ValidationError("项目名长度不为8或者测试人员名称中未包含‘测试’字样")
        return attrs
