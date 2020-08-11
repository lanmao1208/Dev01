import json
import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from .models import Projects
from interfaces.models import Interfaces
from testsuits.models import Testsuits
from .serializers import ProjectsModelSerializer, ProjectsNamesModelSerializer, InterfacesByProjectIdModelSerializer1


class IndexPage(APIView):
    """
    类视图
    1、一定要继承View父类，或者View的子类
    2、可以定义get、post、put、delete方法，来分别实现GET请求、POST请求、PUT请求、DELETE请求
    3、get、post、put、delete方法名称固定，且均为小写
    4、实例方法的第二个参数为HttpRequest对象
    5、一定要返回HttpResponse对象或者HttpResponse子类对象
    """

    def get(self, request):
        # 假设data数据是从数据库从读取的
        # a.render函数主要用于渲染模板生成一个html页面
        # b.第一个参数为request
        # b.第二个参数为在templates目录下的目录名
        # c.第三个参数为context，只能传字典
        # d.locals()函数能获取当前命名空间中的所有变量信息，然后存放在一个字典中
        # return render(request, 'demo.html')
        # return render(request, 'index.html', locals())
        # e.JsonResponse是HttpResponse的子类
        # 第一个参数为字典或者嵌套字典的列表，如果为非字典类型，需要将safe设置为False
        # 会返回一个json的字符串
        # 模型类对象方法
        res = Projects.objects.all()
        # 第二种查询方法
        # res = Projects.objects.filter(id__lte=4)
        # return HttpResponse("<h2>GET请求：查询成功{}</h2>".format(res))

        one_obj = ProjectsModelSerializer(instance=res, many=True)
        return Response(one_obj.data, status=201)

    def post(self, request):
        # a.可以使用request.POST方法，去获取application/x-www-urlencoded类型的参数
        # b.可以使用request.body方法，去获取application/json类型的参数
        # c.可以使用request.META方法，获取请求头参数，key为HTTP_请求头key的大写
        # times = datetime.datetime
        # 模型类对象方法
        # pro_one = Projects(name="django作业1{}".format(times),leader="负责人1{}".format(times),
        #          tester="测试人员1{}".format(times),programmer="开发人员1{}".format(times))
        # 使用save()方法提交
        # pro_one.save()
        # 创建方法二，使用查询集的Projects.objects.create()方法
        # pro_two = Projects.objects.create(name="django作业2{}".format(times),leader="负责人2{}".format(times),
        #          tester="测试人员2{}".format(times),programmer="开发人员2{}".format(times))
        # return HttpResponse("<h2>POST请求：创建成功</h2>")
        create_data = request.body
        create_json_data = json.loads(create_data)
        rsf = ProjectsModelSerializer(data=create_json_data)
        rsf.is_valid(raise_exception=True)
        rsf.save()
        return Response(rsf.data, status=201)

    def put(self, request):
        # a.HttpResponse对象，第一个参数为字符串类型或者字节类型，会将字符串内容返回到前端
        # b.可以使用content_type来指定响应体的内容类型
        # c.可以使用status参数来指定响应状态码
        # return HttpResponse("<h2>PUT请求：欢迎测试开发测试的大佬们！</h2>")
        # 获取id=1的数值，模型类对象方法
        # res1 = Projects.objects.get(id=1)
        # 重新赋值
        # res1.name = "修改后id1的name值"
        # 保存并提交
        # res1.save()
        # 第二种更新方法
        # res2 = Projects.objects.filter(id = 2).update(name = "修改后id2的name值")
        # return HttpResponse("<h2>PUT请求：更新成功{}和{}</h2>".format(Projects.objects.get(id=1),
        #                                                       Projects.objects.get(id=2)), content_type='application/json', status=200)
        pass

    def delete(self, request):
        # 查询并删除，模型类对象方法
        # res1 = Projects.objects.get(id=1)
        # res1.delete()
        # 第二种删除方法
        # res2 = Projects.objects.filter(id = 2).delete()
        # return HttpResponse("<h2>DELETE请求：删除成功</h2>")
        pass




# from utils.pagination import MyPagination
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')


class ProjectsViewSet(viewsets.ModelViewSet):
    """
    list:
    获取项目的列表信息

    retrive:
    获取项目详情数据

    create:
    创建项目

    names:
    获取项目名称

    interfaces:
    获取某个项目下的接口名称
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     results = response.data['results']
    #     for item in results:
    #         # item为一条项目数据所在的字典
    #         # 需要获取当前项目所属的接口总数、用例总数、配置总数、套件总数
    #         project_id = item.get('id')
    #         # interface_count = Interfaces.objects.filter(project_id=project_id).count()
    #         # interface_qs = Interfaces.objects.filter(project_id=project_id)
    #         # for obj in interface_qs:
    #         #     interface_id = obj.id
    #         #     TestCase.ojbects.filter(interface_id=interface_id).count()
    #
    #         # a.使用.annotate()方法，那么会自动使用当前模型类的主键作为分组条件
    #         # b.使用.annotate()方法里可以添加聚合函数，计算的名称为一般从表模型类名小写（可以在外键字段上设置related_name）
    #         # c.values可以指定需要查询的字段（默认为所用字段）
    #         # d.可以给聚合函数指定别名，默认为testcases__count
    #         # 指定查询创建时间最早或者最晚的测试用例，注意参数和参数中间用双下划线分割，另外还可以计算平均值等
    #         # 聚合函数中第一个为从表表名小写，第二个字段为从表字段名小写
    #         # annotate(testcases=Min('testcases__create_time')) or annotate(testcases=Max('testcases__create_time'))
    #         # values调用在annotate方法后面时，values('id', 'testcases')方法中输出你想要的输出的字段，此处为id和testcases字段
    #         # values调用在annotate方法前面时，values('id')会自动输出testcases字段，查询结果相同
    #         interfaces_qs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).filter(project_id=project_id)
    #         # interfaces_obj = Interfaces.objects.annotate(testcases=Count('testcases')).values('id', 'testcases').filter(project_id=project_id)
    #
    #         Interfaces.objects.annotate(Count('testcases'))
    #     pass
    # 如果父类中有提供相关的逻辑
    # 1、绝大部分不需要修改，只有少量要修改的，直接对父类中的action进行拓展
    # 2、绝大部分都需要修改的话，那么直接自定义即可
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        data_list = []
        for item in results:
            # item为一条项目数据所在的字典
            # 需要获取当前项目所属的接口总数、用例总数、配置总数、套件总数
            project_id = item.get('id')
            # interface_count = Interfaces.objects.filter(project_id=project_id).count()
            # interface_qs = Interfaces.objects.filter(project_id=project_id)
            # for obj in interface_qs:
            #     interface_id = obj.id
            #     TestCase.ojbects.filter(interface_id=interface_id).count()

            # a.使用.annotate()方法，那么会自动使用当前模型类的主键作为分组条件
            # b.使用.annotate()方法里可以添加聚合函数，计算的名称为一般从表模型类名小写（可以在外键字段上设置related_name）
            # c.values可以指定需要查询的字段（默认为所用字段）
            # d.可以给聚合函数指定别名，默认为testcases__count
            # e.如果values放在annotate前面，那么聚合运算的字段不需要在values中添加，放在后面需要
            # interfaces_obj = Interfaces.objects.annotate(testcases1=Count('testcases')).values('id', 'testcases1').\
            #     filter(project_id=project_id)

            interface_testcase_qs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')). \
                filter(project_id=project_id)

            # 获取项目下的接口总数
            interfaces_count = interface_testcase_qs.count()

            # 定义初始用例总数为0
            testcases_count = 0
            for one_dict in interface_testcase_qs:
                testcases_count += one_dict.get('testcases')

            # 获取项目下的配置总数
            interface_configure_qs = Interfaces.objects.values('id').annotate(configures=Count('configures')). \
                filter(project_id=project_id)
            configures_count = 0
            for one_dict in interface_configure_qs:
                configures_count += one_dict.get('configures')

            # 获取项目下套件总数
            testsuites_count = Testsuits.objects.filter(project_id=project_id).count()

            item['interfaces'] = interfaces_count
            item['testcases'] = testcases_count
            item['testsuits'] = testsuites_count
            item['configures'] = configures_count
            data_list.append(item)

        response.data['results'] = data_list

        return response


    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = Interfaces.objects.filter(projects=instance)
        serializer_obj = self.get_serializer(instance=instance)
        # 进行过滤和分页操作
        return Response(serializer_obj.data)

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNamesModelSerializer
        elif self.action == 'interfaces':
            # return InterfacesByProjectIdModelSerializer
            return InterfacesByProjectIdModelSerializer1
        else:
            return self.serializer_class
