import os
import json
from datetime import datetime

from rest_framework.decorators import action
from rest_framework import permissions
from django.conf import settings

import logging
from rest_framework.response import Response
from utils.currency_class import Currency_View_Class
from utils import common
from interfaces.models import Interfaces
from .serializers import InterfacesModelSerializer,TestcasesByInterfacesIdModelSerializer,ConfiguresByInterfacesIdModelSerializer
from testcases.serializers import TestcasesRunSerializer
from envs.models import Envs
from testcases.models import Testcases
from configures.models import Configures

# from utils.pagination import MyPagination
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')


class InterfacesViewSet(Currency_View_Class):
    """
    name:
        获取所有接口的id，name
    list:
        获取所有接口列表信息
    create:
        创建接口
    retrieve:
        获取接口详情
    destory:
        删除接口
    update:
        更新接口
    """
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        """
        testcases: 用例总数
        configures: 配置总数
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().list(self, request, *args, **kwargs)
        dict_data = response.data["results"]
        for item in dict_data:
            # 获取接口id
            interface_id = item.get('id')
            # 用例总数
            testcases_count = Testcases.objects.filter(interface_id=interface_id).count()
            # 配置总数
            configures_count = Configures.objects.filter(interface_id=interface_id).count()
            results_data = {"testcases": testcases_count, "configures": configures_count}
            item.update(results_data)
        response.data["results"] = dict_data
        return response

    @action(methods=['get'],detail=True)
    def testcases(self, request, *args, **kwargs):
        # instance = self.get_object()
        # serializer_obj = self.get_serializer(instance=instance)
        # return Response(serializer_obj.data["testcases"])
        # response = self.retrieve(request, *args, **kwargs)
        # response.data = response.data["testcases"]
        # return response
        return self.currency_action_def(request, "testcases", *args, **kwargs)

    @action(methods=['get'],detail=True)
    def configures(self, request, *args, **kwargs):
        # instance = self.get_object()
        # serializer_obj = self.get_serializer(instance=instance)
        # return Response(serializer_obj.data["configures"])
        # response = self.retrieve(request, *args, **kwargs)
        # response.data = response.data["configures"]
        # return response
        return self.currency_action_def(request, "configures",*args, **kwargs)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 取出并构造参数
        instance = self.get_object()
        response = super().create(request, *args, **kwargs)
        env_id = response.data.serializer.validated_data.get('env_id')
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建一个以时间戳命名的路径
        os.mkdir(testcase_dir_path)
        env = Envs.objects.filter(id=env_id).first()
        interfaces_qs = Interfaces.objects.filter(instance)
        runner_testcases_obj = []
        testcase_qs = Testcases.objects.filter(interface=interfaces_qs)
        if testcase_qs.exists():
            runner_testcases_obj.extend(list(testcase_qs))
        if len(runner_testcases_obj) == 0:
            data = {
                'ret': False,
                'msg': '该项目下无用例存在，无法运行'
            }
            return Response(data, status=400)
        for testcase_obj in runner_testcases_obj:
            # 生成yaml用例文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)
        # 运行用例（生成报告）
        common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == 'testcases':
            return TestcasesByInterfacesIdModelSerializer
        elif self.action == 'configures':
            return ConfiguresByInterfacesIdModelSerializer
        elif self.action == 'run':
            return TestcasesRunSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        # 重写父类的perform_create方法，使用run动作时不进行保存操作
        if self.action == 'run':
            pass
        else:
            serializer.save()


