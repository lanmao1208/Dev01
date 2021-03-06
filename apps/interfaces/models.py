from django.db import models
from utils.base_models import BaseModel

# Create your models here.
# 一个mysql软件中，可以有多个数据库
# 一个数据库中，可以有多张数据表
# 一张数据表中，有多条数据（多条记录）以及多个字段（多个列）


from django.db import models

from utils.base_models import BaseModel


class Interfaces(BaseModel):
    """
    1、可以在子应用projects/models.py文件中，来定义数据模型
    2、一个数据模型类对应一个数据表
    3、数据模型类，需要继承Model父类或者Model子类
    4、在数据模型类中，添加的类属性（Field对象）来对应数据表中的字段
    5、创建完数据库模型类之后，需要迁移才能生成数据表
    a.生成迁移脚本，放在projects/migrations目录中：python manage.py makemigrations
    b.执行迁移脚本：python manage.py migrate
    c.如果不添加选项，那么会将所有子应用进行迁移
    6、会自动创建字段名为id的类属性，自增、主键、非空
    7、只要某一个字段中primary_key=True，那么Django就不会自动创建id字段，会使用自定义的
    8、CharField -> varchar
    IntegerField -> int
    TextField -> text
    9、verbose_name为个性化信息
    10、help_text帮助文本信息，在api接口文档平台和admin后端站点中会用于提示，往往跟verbose_name一致
    11、unique用于指定唯一键，默认为False
    12、CharField至少要指定一个max_length必传参数，代表此字段的最大长度，不能为负数
    13、null指定数据在保存时是否可以为空，默认不能为空，如果null=True，那么可以为空值
    14、blank指定前端用户在创建数据时，是否需要传递，默认需要传递，如果不传递，需要blank设置为True
    15、default为某一个字段指定默认值，往往会跟blank一起使用，TextField无长度限制
    16、DateTimeField可以添加auto_now_add选项，django会自动添加创建记录时的时间
    17、DateTimeField可以添加auto_now选项，django会自动添加更新记录时的时间
    18、执行迁移脚本之后，生成的数据表名默认为 子应用名_模型类名小写
    19、可以在模型类下定义Meta子类，Meta子类名称固定
    20、可以使用db_table类属性，来指定表名
    21、verbose_name指定表的个性化描述
    """
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('接口名称', max_length=200, unique=True, help_text='接口名称')
    # 外键字段名称,可设置related_name = "指定名"，指定名为父表在ModelSerializer类中打印该表属性时所用的指定属性名称
    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE,
                                related_name='interfaces', help_text='所属项目')
    tester = models.CharField('测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField('简要描述', max_length=200, null=True, blank=True, help_text='简要描述')

    class Meta:
        db_table = 'tb_interfaces'
        verbose_name = '接口信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
