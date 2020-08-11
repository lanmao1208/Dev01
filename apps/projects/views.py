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
from .serializers import ProjectsModelSerializer, ProjectsNamesModelSerializer, InterfacesByProjectIdModelSerializer

# 定义日志器用于记录日志
logger = logging.getLogger('mytest')


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_filter = ['id', 'name', 'leader', 'programmer', 'tester']

    # pagination_class =

    # 如果父类中有提供相关的逻辑
    # 1、绝大部分不需要修改，只有少量要修改的，直接对父类中的action进行拓展
    # 2、绝大部分都需要修改的话，那么直接自定义即可
    def list(self, request, *args, **kwargs):
        # 获取项目列表信息时, 获取当前项目所属的接口总数、用例总数、配置总数、套件总数
        # 需要将创建时间格式化为 2019年06月24 00:36:55
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        data_list = []
        # item为一条项目数据所在的字典
        for item in results:
            # 项目id
            project_id = item.get('id')
            interfaces_qs = Interfaces.objects.filter(project_id=project_id)
            # 指定项目下的接口总数
            interfaces_num = interfaces_qs.count()
            # 指定项目下的用例总数
            testcases_query_set = interfaces_qs.values('id').annotate(testcases_num=Count('testcases'))
            testcases_num = sum([item.get('testcases_num') for item in testcases_query_set])
            # 指定项目下的配置总数
            configures_query_set = interfaces_qs.values('id').annotate(configures_num=Count('configures'))
            configures_num = sum([item.get('configures_num') for item in configures_query_set])
            # 指定项目下的套件总数
            testsuits_num = Testsuits.objects.filter(project_id=project_id).count()
            # 格式化创建时间
            item["create_time"] = "2019年06月24 00:36:55"
            item["interfaces"] = interfaces_num
            item["testcases"] = testcases_num
            item["configures"] = configures_num
            item["testsuits"] = testsuits_num
            data_list.append(item)
        response.data['results'] = data_list
        return response


    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        # 在下拉框拉取数据时，不需要进行分页操作
        # instance = self.get_object()
        # qs = Interfaces.objects.filter(projects=instance)
        # serializer_obj = self.get_serializer(instance=instance)
        # # 进行过滤和分页操作
        # return Response(serializer_obj.data)
        qs = self.retrieve(request, *args, **kwargs)
        return Response(qs.data['interfaces'])

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectsNamesModelSerializer
        elif self.action == 'interfaces':
            return InterfacesByProjectIdModelSerializer
        else:
            return self.serializer_class
