from rest_framework import serializers
from rest_framework import validators
from .models import Projects
from projects.models import Projects


# from interfaces.serializers import InterfaceModelSerializer


# ModelSerializer方法
class ProjectsModelSerializer(serializers.ModelSerializer):
    """
    通过父表获取子表的信息
    a.默认可以使用子表模型类名小写_set
    interfaces_set = InterfacesModelSerializer(label='所拥有的接口', many=True)
    b.如果某个字段返回的结果有多条，那么需要添加many=True参数
    c.如果模型类中外键字段定义了related_name参数，那么会使用这个名称作为字段名
    interfaces_set = serializers.StringRelatedField(many=True)
    """
    # interfaces_set = InterfaceModelSerializer(label="所拥有的接口", many=True)
    # creat_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    # updata_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    # Meta类名固定，用于存放当前类的一些元素信息
    class Meta:
        """
        b.需要在Meta内部类这两个指定model类属性：需要按照哪一个模型类来创建
        c.fields类属性来指定，模型类中哪些字段需要输入或输出
        d.默认id主键，会添加read_only=True
        e.create_time和update_time，会添加read_only=True
        可以将需要输入或者输出的字段，在元组中指定
        定义的所有序列化器字段，必须得添加到fields元组中，模型类中未定义的字段也需要添加
        fields = ('id', 'name', 'leader', 'tester', 'programmer', 'interfaces_set', 'create_time', 'update_time', 'email')
        把需要排除的字段放在exclude中
        exclude = ('desc', 'create_time')
        可以在read_only_fields中指定需要进行read_only=True的字段
        """
        model = Projects
        # fields = '__all__'
        fields = ('id','name','leader','tester','programmer','desc')
        # exclude = ('creat_time', 'updata_time')
        # read_only_fields = ('creat_time', 'updata_time')
