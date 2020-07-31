from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from interfaces.models import Interfaces
from .serializers_homewrok import InterfacesModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from utils.pagination import MyPagination


class InterfacesModelPage(GenericAPIView):
    # 指定queryset，当前接口中需要使用到的查询集（查询集对象）
    # 指定serializer_class，当前接口中需要使用到的序列化器类
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer

    # 在filter_backends中指定OrderingFilter来实现排序功能
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('name',)
    # 在ordering_fields来指定需要排序的字段
    ordering_fields = ('name',)
    # 在视图中指定分页引擎类,优先级比全局指定要高
    pagination_class = MyPagination

    def get(self, request):
        result = {}
        try:
            # 使用.get_queryset()方法，获取查询集对象，并进行过滤
            res = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(res)
            # 如果分页不为none，进行分页操作
            if page is not None:
                one_obj = self.get_serializer(instance=page, many=True)
                return self.get_paginated_response(one_obj.data)
            one_obj = self.get_serializer(instance=res, many=True)
            return Response(one_obj.data, status=status.HTTP_200_OK)
        except Exception as e:
            result["msg"] = "查询失败，指定ID不存在"
            result["code"] = 1
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
