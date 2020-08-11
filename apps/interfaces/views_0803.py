import logging
from interfaces.models import Interfaces
from .serializers import InterfacesModelSerializer, InterfacesNameModelSerializer, InterfacesByProjectsIdSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from utils.pagination import MyPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

# from utils.pagination import MyPagination
# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')


class InterfacesViewSet(viewsets.ModelViewSet):
    """
    list:
        获取项目的列表信息
    retrive:
        获取项目详情数据
    create:
        创建项目
    names:
        获取项目名称
    interfaces：
        获取某个项目下的接口名称
    """
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer
    # authentication_classes在视图中指定认证方式，可以在列表中添加多个认证类
    # 视图中指定的认证方式优先级大于全局指定的认证方式
    # authentication_classes = []
    # permission_classes在视图中指定权限，可以在列表中添加多个权限类
    # 视图中指定的权限优先级大于全局指定的权限(setting.py文件)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('id','name')
    ordering_fields = ('id','name')
    pagination_class = MyPagination

    # a.可以使用action装饰器去自定义动作方法
    # b.methods参数默认为['get']，可以定义支持请求方式['get', 'post', 'put']
    # c.detail参数为必传参数，指定是否为详情数据（如果需要传递主键id那么，detail=True，否则detail=False）
    # d.url_path指定url路径部分，默认为action名称（当前为names）
    # e.url_name指定url的名称，默认为action名称（当前为names，完整路由名称为names-list）
    @action(detail=False)
    def names(self, request):
        # 分页操作
        res = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(res)
        if page is not None:
            result = self.get_serializer(instance=page, many=True)
            data = result.data
            logger.debug(data)
            return self.get_paginated_response(data)
        result = InterfacesNameModelSerializer(instance=self.get_queryset(), many=True)
        data = result.data
        logger.debug(data)
        return Response(data)

    @action(detail=True)
    def interfaces(self, request, *args, **kwargs):
        # 分页操作
        instance = self.get_object()
        result = Interfaces.objects.filter(projects=instance)
        page = self.paginate_queryset(result)
        if page is not None:
            result = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(result.data)
        result = self.get_serializer(instance=instance)
        return Response(result.data)


    def get_serializer_class(self):
        if self.action == 'names':
            return InterfacesNameModelSerializer
        elif self.action == 'interfaces':
            return InterfacesByProjectsIdSerializer
        else:
            return self.serializer_class
