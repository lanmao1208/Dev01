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
from interfaces.models import Interfaces
from .serializers import ProjectsModelSerializer, ProjectsNamesModelSerializer, InterfacesByProjectIdModelSerializer1

# 定义日志器用于记录日志
logger = logging.getLogger('mytest')


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # 获取项目列表信息时, 获取当前项目所属的接口总数、用例总数、配置总数、套件总数
        # 需要将创建时间格式化为 2019年06月24 00:36:55
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        # item为一条项目数据所在的字典
        for i in range(len(results)):
            # 项目id
            project_id = results[i].get('id')
            # 用例总数
            testcases_counts= Interfaces.objects.annotate(testcases1 = Count('testcases')).values('id', 'testcases1').filter(project_id=project_id)
            for item in testcases_counts.values():
                if item['id'] == project_id:
                    results[i]["testcases_counts"] = "一共{}条测试用例".format(item["testcases1"])
            # 接口总数
            interfaces_counts= Interfaces.objects.annotate(interfaces1 = Count('desc')).values('id', 'interfaces1').filter(project_id=project_id)
            for item in interfaces_counts.values():
                if item['id'] == project_id:
                    results[i]["interfaces_counts"] = "一共{}个接口".format(item["interfaces1"])
            # 配置总数
            configures_counts = Interfaces.objects.annotate(configures1 = Count('configures')).values('id', 'configures1').filter(project_id=project_id)
            for item in configures_counts.values():
                if item['id'] == project_id:
                    results[i]["configures_counts"] = "一共{}条配置".format(item["configures1"])
            # 套件总数
            # results[i]["testsuits_counts"] = Interfaces.objects.annotate(testsuits1 = Count('include')).values('id', 'include').filter(project_id=project_id)
            # 格式化创建时间
            results[i]["create_time"] = "2019年06月24 00:36:55"
        return Response(results)

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
