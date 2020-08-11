import json
import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from .models import Projects
# from utils.pagination import N
from interfaces.models import Interfaces
from testsuits.models import Testsuits
from .serializers import ProjectsModelSerializer, ProjectsNamesModelSerializer, InterfacesByProjectIdModelSerializer1

# 定义日志器用于记录日志
logger = logging.getLogger('mytest')


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_filter = ['id', 'name', 'leader', 'programmer', 'tester']

    # pagination_class =

    def list(self, request, *args, **kwargs):
        # 获取项目列表信息时, 获取当前项目所属的接口总数、用例总数、配置总数、套件总数
        # 需要将创建时间格式化为 2019年06月24 00:36:55
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        # item为一条项目数据所在的字典
        for i in range(len(results)):
            # 项目id
            project_id = results[i].get('id')
            # 指定项目下的用例总数
            testcases_counts= Interfaces.objects.annotate(testcases1 = Count('testcases')).values('id', 'testcases1').filter(project_id=project_id)
            for item in testcases_counts.values():
                if item['id'] == project_id:
                    results[i]["testcases_counts"] = "一共{}条测试用例".format(item["testcases1"])
            # 指定项目下的接口总数
            interfaces_counts= Interfaces.objects.annotate(interfaces1 = Count('desc')).values('id', 'interfaces1').filter(project_id=project_id)
            for item in interfaces_counts.values():
                if item['id'] == project_id:
                    results[i]["interfaces_counts"] = "一共{}个接口".format(item["interfaces1"])
            # 指定项目下的配置总数
            configures_counts = Interfaces.objects.annotate(configures1 = Count('configures')).values('id', 'configures1').filter(project_id=project_id)
            for item in configures_counts.values():
                if item['id'] == project_id:
                    results[i]["configures_counts"] = "一共{}条配置".format(item["configures1"])
            # 指定项目下的套件总数
            # results[i]["testsuits_counts"] = Interfaces.objects.annotate(testsuits1 = Count('include')).values('id', 'include').filter(project_id=project_id)
            # 格式化创建时间
            results[i]["create_time"] = "2019年06月24 00:36:55"
        return Response(results)

    # 如果父类中有提供相关的逻辑
    # 1、绝大部分不需要修改，只有少量要修改的，直接对父类中的action进行拓展
    # 2、绝大部分都需要修改的话，那么直接自定义即可
    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     results = response.data['results']
    #     data_list = []
    #     for item in results:
    #         # item为一条项目数据所在的字典
    #         # 需要获取当前项目所属的接口总数、用例总数、配置总数、套件总数
    #         project_id = item.get('id')
    #         # 获取当前项目测试用例查询集
    #         interface_testcase_qs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')). \
    #             filter(project_id=project_id)
    #
    #         # 获取项目下的接口总数
    #         interfaces_count = interface_testcase_qs.count()
    #
    #         # 定义初始用例总数为0
    #         testcases_count = 0
    #         for one_dict in interface_testcase_qs:
    #             testcases_count += one_dict.get('testcases')
    #
    #         # 获取项目下的配置总数
    #         interface_configure_qs = Interfaces.objects.values('id').annotate(configures=Count('configures')). \
    #             filter(project_id=project_id)
    #         configures_count = 0
    #         for one_dict in interface_configure_qs:
    #             configures_count += one_dict.get('configures')
    #
    #         # 获取项目下套件总数
    #         testsuites_count = Testsuits.objects.filter(project_id=project_id).count()
    #
    #         item['interfaces'] = interfaces_count
    #         item['testcases'] = testcases_count
    #         item['testsuits'] = testsuites_count
    #         item['configures'] = configures_count
    #         data_list.append(item)
    #
    #     response.data['results'] = data_list
    #
    #     return response

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
            return InterfacesByProjectIdModelSerializer1
        else:
            return self.serializer_class
