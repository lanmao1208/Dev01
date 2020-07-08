from rest_framework import serializers
# 一定要继承父类 序列化器类
class ProjectSerializer(serializers.Serializer):
    # 定义序列化输出条件
    name = serializers.CharField(max_length=200,label='接口名称',help_text='接口名称')
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员')
    desc = serializers.CharField(max_length=200, label='简要描述', help_text='简要描述')
