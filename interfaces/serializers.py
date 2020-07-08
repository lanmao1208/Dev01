from rest_framework import serializers
# 一定要继承父类 序列化器类
class InterfaceSerializer(serializers.Serializer):
    # 定义序列化输出条件
    name = serializers.CharField(max_length=200,label='接口名称',help_text='接口名称')
    projects_id = serializers.IntegerField(label='所属项目ID',help_text='所属项目ID')
    tester = serializers.CharField(max_length=50, label='测试人员', help_text='测试人员')
    desc = serializers.CharField(max_length=200, label='简要描述', help_text='简要描述')
    # # 输出时间
    # creat_time = serializers.DateTimeField(format='%Y-%M-%D %H:%M:%S',required=True,read_only=True)
    # updata_time = serializers.DateTimeField(format='%Y-%M-%D %H:%M:%S',required=True,read_only=True)
