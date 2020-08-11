import logging
from interfaces.models import Interfaces
from .serializers import InterfacesModelSerializer,TestcasesByInterfacesIdModelSerializer,ConfiguresByInterfacesIdModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from utils.currency_class import Currency_View_Class
from utils.pagination import MyPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
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
        dict_data = response.data["result"]
        for item in dict_data:
            # 获取接口id
            interfaces_id = item.get('id')
            # 用例总数
            testcases_count = Testcases.objects.filter(interfaces_id=interfaces_id).count()
            # 配置总数
            configures_count = Configures.objects.filter(interfaces_id=interfaces_id).count()
            result_data = {"testcases": testcases_count, "configures": configures_count}
            item.update(result_data)
        response.data["result"] = dict_data
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

    def get_serializer_class(self):
        if self.action == 'testcases':
            return TestcasesByInterfacesIdModelSerializer
        elif self.action == 'configures':
            return ConfiguresByInterfacesIdModelSerializer
        else:
            return self.serializer_class
