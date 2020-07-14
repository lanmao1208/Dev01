from rest_framework import serializers
from rest_framework import validators
from .models import Interfaces


# from projects.models import Projects


# 定义筛选条件类
# value为前端输入待效验的值
def is_name_contain_x(value):
    if "x" in value:
        # 不符合效验条件，必须抛出ValidationError该异常，不可变
        raise serializers.ValidationError("项目名称中不能包含x")


# 一定要继承父类 序列化器类
# Serializer方法
class InterfaceSerializer(serializers.Serializer):
    """
    可以定义序列化器类，来实现序列化和反序列化操作
    a.一定要继承serializers.Serializer或者Serializer的子类
    b.默认情况下，可以定义序列化器字段，序列化器字段名要与模型类中字段名相同
    c.默认情况下，定义几个序列化器字段，那么就会返回几个数据（到前端，序列化输出的过程），前端也必须得传递这几个字段（反序列化过程）
        定义序列化输出条件
    d.CharField、BooleanField、IntegerField与模型类中的字段类型一一对应
    e.required参数默认为None，指定前端必须得传此字段，如果设置为False的话，前端可以不传此字段
    f.label和help_text -> verbose_name和help_text一一对应
    g.allow_null指定前端传递参数时可以传空值
    CharField字段，max_length指定该字段最大字节个数，min_length指定该字段最小字节个数
    validators字段指定该属性的效验条件，只能传入列表
    validators字段中UniqueValidator为第一个参数，是自带的效验规则(最常用)，其中queryset传入该项目所有的查询集，message传入该序列器效验不通过后打印的文字
    validators字段中自定义效验规则，不能调用，只能写方法名(如果是创建效验类进行效验，则方法需要放在__call__方法中)
    validators字段的效验规则会全部执行，即时其中某个规则效验失败
    leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人')
    h.如果某个字段指定read_only=True，那么此字段，前端在创建数据时（反序列化过程）可以不用传，但是一定会输出（序列化过程）
    i.字段不能同时指定read_only=True, required=True
    leader = serializers.CharField(max_length=200, label='项目负责人', help_text='项目负责人', read_only=True, required=True)
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员')
    j.如果某个字段指定write_only=True，那么此字段只能进行反序列化输入，而不会输出（创建数据时必须得传，但是不返回）
    k.可以给字段添加error_messages参数，为字典类型，字典的key为校验的参数名，值为校验失败之后错误提示
    k.一个字段不同同时指定write_only=True, read_only=True
    tester = serializers.CharField(max_length=200, label='测试人员', help_text='测试人员', write_only=True, read_only=True)
    """
    name = serializers.CharField(max_length=200, label='接口名称', help_text='接口名称', min_length=2,
                                 validators=[validators.UniqueValidator(
                                     queryset=Interfaces.objects.all(), message="项目名称不能少于2个字符"),
                                     is_name_contain_x])
    projects_id = serializers.IntegerField(label='所属项目ID', help_text='所属项目ID')
    # allow_null=True 允许该字段传Null参数
    # allow_blank=True 允许该字段传空字符串("")
    # required=False/write_only=True 允许该字段不传
    # 只写入不输出writer_only = True ,只输出不写入 read_only = True
    tester = serializers.CharField(max_length=50, label='测试人员', help_text='测试人员')
    desc = serializers.CharField(max_length=200, label='简要描述', help_text='简要描述', write_only=True,
                                 error_messages={"required": "该字段必传", "max_length": "长度不能操作200个字节"})
    # 输出时间
    creat_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)
    updata_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    # 序列化器类中书写单字段效验规则，命名规则必须为validate_字段名
    # 不需要添加，自动运行该效验规则

    def validate_name(self, value):
        if "x" in value:
            # 不符合效验条件，必须抛出ValidationError该异常，不可变
            raise serializers.ValidationError("项目名称中不能包含x")
        # 和序列化器类以外自定义效验方法不同，这里必须返回效验之后的值
        return value

    # 联合效验，多字段效验，效验顺序为最后
    # 在序列化器类中对多字段进行联合校验
    # a.校验方法名称为：validate
    # b.一定要返回校验之后的值
    # c.attrs为前端输入的待校验参数
    def validate(self, attrs):
        if len(attrs["name"]) != 8 or "测试" not in attrs:
            raise serializers.ValidationError("项目名长度不为8或者测试人员名称中未包含‘测试’字样")
        return attrs

    # 重写序列化器类中的create方法
    def create(self, validated_data):
        # validated_data参数为校验通过之后的数据
        # 必须将创建成功的模型类对象返回
        # obj = Interfaces.objects.create(**validated_data)
        # 父类super的create方法传参拆包会报错
        obj = super().create(validated_data)
        return obj

    # 重写序列化器类中的update方法
    def update(self, instance, validated_data):
        # instance为待更新的模型类对象
        # validated_data参数为校验通过之后的数据
        # 必须将更新成功的模型类对象返回
        instance.name = validated_data.get('name') or instance.name
        instance.projects_id = validated_data.get('projects_id') or instance.projects_id
        instance.tester = validated_data.get('tester') or instance.tester
        instance.desc = validated_data.get('desc') or instance.desc
        instance.save()
        return instance


# ModelSerializer方法
class InterfaceModelSerializer(serializers.ModelSerializer):
    """
    如果在模型序列化器类中显示指定了模型类中的某个字段，那么会将自动生成的字段覆盖掉
    name = serializers.CharField(max_length=10, label='项目名称', help_text='项目名称', min_length=2,
                                 validators=[validators.UniqueValidator(queryset=Projects.objects.all(), message='项目已存在')])
    可以再该类下重新定义model中属性，重新定义后会覆盖原有属性
    1.projects字段输出父表中主键id值
        projects = serializers.PrimaryKeyRelatedField(help_text='所属项目', label='所属项目', queryset=Projects.objects.all())
    2.自动调用模型类中__str__()方法，通过projects字段输出
        projects = serializers.StringRelatedField()
    3.projects字段输出父表中slug_field的指定字段，该处为leader
        projects = serializers.SlugRelatedField(slug_field="leader",read_only=True)
    4.可以将某个序列化器对象定义为字段，支持fields中的所有参数,
        projects = ProjectsModelSerializer(label='所属项目信息', help_text='所属项目信息', read_only=True)
    部分注释可以观看projects/serializer文件
    """
    projects = serializers.PrimaryKeyRelatedField()

    # Meta类名固定，用于存放当前类的一些元素信息
    class Meta:
        """
        1.不能调用，只能使用模型类名称
        2.可以进入ipython模式查看相关信息
            1.使用python manage.py shell -i ipython进入ipython(需要提前安装ipython)
            2.from interfaces.serializers import InterfaceModelSerializer导入
            3.InterfaceModelSerializer()调用方法，查看信息
        3.fields = '__all__' 传递全部字段
          fields = (字段名1,字段名2,.....)只传递元祖内字段
          exclude = (字段名1,.....)只传递除元祖内字段
          read_only_fields = (字段名1,.....)元祖内字段统一设置read_only属性

        """
        #
        model = Interfaces
        fields = '__all__'
        # 改写属性:可以修改属性，也可以添加不存在的属性
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
        read_only_fields = ('creat_time', 'updata_time')


    # 序列化器类中书写单字段效验规则，命名规则必须为validate_字段名
    # 不需要添加，自动运行该效验规则

    def validate_name(self, value):
        if "x" in value:
            # 不符合效验条件，必须抛出ValidationError该异常，不可变
            raise serializers.ValidationError("项目名称中不能包含x")
        # 和序列化器类以外自定义效验方法不同，这里必须返回效验之后的值
        return value

    # 联合效验，多字段效验，效验顺序为最后
    # 在序列化器类中对多字段进行联合校验
    # a.校验方法名称为：validate
    # b.一定要返回校验之后的值
    # c.attrs为前端输入的待校验参数
    def validate(self, attrs):
        if len(attrs["name"]) != 8 or "测试" not in attrs:
            raise serializers.ValidationError("项目名长度不为8或者测试人员名称中未包含‘测试’字样")
        return attrs