import json
from django.http import JsonResponse, Http404
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.shortcuts import render
from interfaces.models import Interfaces
from django.db import connections
from .serializers import InterfacesSerializer
from .serializers import InterfacesModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from utils.pagination import MyPagination
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

"""
序列化器对象中的几个重要属性
一、一定要先执行.is_valid()方法之后才能访问
.errors 获取报错信息
.validated_data 校验通过之后的数据（往往也是数据库中需要保存的数据） 有可能不会过滤write_only

二、可以不用调用.is_valid()方法，也能访问
.data 最终返回给前端的数据
"""


# 1、需要继承APIView
# a.对Django中的View进行了拓展
# b.具备认证、授权、限流、不同请求数据的解析

# 如果要实现过滤、查询、分页等功能，需要继承GenericAPIView
# a.GenericAPIView为APIView的子类，拓展了过滤、查询、分页
class InterfacesPage(APIView):
    """
    类视图
    1、一定要继承View父类，或者View的子类
    2、可以定义get、post、put、delete方法，来分别实现GET请求、POST请求、PUT请求、DELETE请求
    3、get、post、put、delete方法名称固定，且均为小写
    4、实例方法的第二个参数为HttpRequest对象
    5、一定要返回HttpResponse对象或者HttpResponse子类对象
    """

    # renderer_classes = [YAMLRenderer]
    def get(self, request, pk=None):
        """
        1.可以使用序列化器类来进行序列化输出
        a.instance参数可以传模型类对象
        b.instance参数可以传查询集（多条记录），many=True
        c.可以ProjectsSerializer序列化器对象，调用data属性，可以将模型类对象转化为Python中的数据类型
        d.如果未传递many=True参数，那么序列化器对象.data，返回字典，否则返回一个嵌套字典的列表
        e.fitter出来是查询集  get出来是模型类对象
                关联查询
        通过从表信息获取父表信息
        从表模型类小名__从表字段名__查询表达式
        查询集对象，只有使用的时候才进行查询操作（惰性查找）
        qs = Interfaces.objects.filter(interfaces__name__regex='^[0-9]')
        逻辑关系查询
        支持链式查询，可以使用多个filter方法进行过滤
        同一行查询中的多个条件是与的关系
        qs =Interfaces.objects.filter(name__startswith="人").filter(programmer__contains="4")
        qs =Interfaces.objects.filter(name__startswith="人",programmer__contains="4")
        同一行查询中的多个条件是或的关系
        Q(条件)|Q(条件)...
        qs = Interfaces.objects.filter(Q(leader__contains) | Q(programmer_contains = "4"))
        特殊操作
        根据name属性进行排序，不带“-”升序，带“-”降序
        Interfaces.objects.all().order_by('-name')
        :param request:
        :param pk:
        :return:
        """
        # 获取查询对象
        result = {}
        try:
            # pk存在则为指定查询对象
            if pk:
                res = self.pk_validity(pk)
            # 不存在则为查询所有对象
            else:
                res = Interfaces.objects.all()
            one_obj = InterfacesModelSerializer(instance=res, many=True)
            # result["data"] = one_obj.data
            # result["msg"] = "查询成功"
            # result["code"] = 0
            # return JsonResponse(result, safe=False, status=201)
            return Response(one_obj.data, status=status.HTTP_200_OK)
        except Exception as e:
            result["msg"] = "查询失败，指定ID不存在"
            result["code"] = 1
            # return JsonResponse(result, status=400)
            # 2、需要使用DRF中的Response去返回
            # a.对Django中的HttpResponse进行了拓展
            # b.实现了根据请求头中Accept参数来动态返回
            # c.默认情况下，如果不传Accept参数或者创建application/json，那么会返回json格式的数据
            # d.如果Accept参数为text/html，那么会返回可浏览的api页面（html页面）
            # e.Response第一个参数为，经过序列化之后的数据（往往需要使用序列化器对象.data）
            # f.status指定响应状态码
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        1、创建序列化器对象InterfaceSerializer
        a.把前端传递的json格式参数转化为字典之后，传递给data参数
        b.序列化器对象.is_valid()方法，开始进行校验，如果不调用此方法，那么不会进行校验
        c.调用序列化器对象.is_valid()方法，如果校验成功，返回True，否则返回False
        d.必须调用is_valid()方法之后，才能使用.errors属性去获取报错信息，相当于一个字典
        e.必须调用is_valid()方法之后，才能使用.validated_data属性去获取校验通过信息，相当于一个字典
        data传输字典或者字典嵌套列表，instance传输查询集对象或者其他类对象
        用于序列化时，将模型类对象传入instance参数(输出/打印)
        用于反序列化时，将要被反序列化的数据传入data参数(输入/写入)
        :param request:
        :return:
        """
        # 继承ApiView之后，request为Request
        # a.对Django中的HttpRequest进行了拓展
        # b.统一使用Request对象.data属性去获取json格式的参数、form表单参数、FILES
        # c.Django支持的参数获取方式，DRF都支持
        # .GET --> 查询字符串参数 --> .query_params
        # .POST --> x-www-form-encoded
        # .body --> 获取请求体参数
        # d.Request对象.data属性为将请求数据转化为python中的字典（嵌套字典的列表）
        # 此处的data属性为请求类中的data属性，而不是序列化器类中的data属性

        # json格式传入创建需要的参数
        # 继承View父类获取值
        # create_data = request.body
        # 继承APIView父类获取值
        # create_data = request.data
        # 获取查询字符串参数 request.query_params,调试模式下查询框使用(快捷键两下shift键)
        #
        # # 判断传入参数是否为json或者字典格式
        # try:
        #     # a.获取新的项目信息并转化为python中数据类型（字典或者嵌套字典的列表）
        #     create_json_data = json.loads(create_data)
        # except Exception as e:
        #     result["msg"] = "参数错误"
        #     result["code"] = 1
        #     return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)
        result = {}
        rsf = InterfacesModelSerializer(data=request.data)
        # 效验数据是否符合接口要求的参数设置
        try:
            # 创建序列化器对象
            rsf.is_valid(raise_exception=True)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            result.update(rsf.errors)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        # 效验通过后进行创建
        # c.创建项目,validated_data如果缺少某些字段，既不会报错也不会保存
        # Interfaces.objects.create(**rsf.validated_data)
        # 使用序列化器save方法，传递的关键字参数，会自动添加到create()方法，validated_data字典中
        # rsf.save(user = "创建人名字")
        rsf.save()
        result.update(rsf.data)
        result["msg"] = "创建成功"
        result["code"] = 0
        return Response(result, status=status.HTTP_201_CREATED)
        # return JsonResponse(result,safe=False,status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        result = {}
        # 更新id为pk，更新内容通过json传递
        res = self.pk_validity(pk)
        # 如果在定义序列化器对象时，同时指定instance和data参数
        # a.调用序列化器对象.save()方法，会自动调用序列化器类中的update方法
        rsf = InterfacesModelSerializer(instance=res, data=request.data)
        # 效验数据是否符合接口要求的参数设置
        try:
            rsf.is_valid(raise_exception=True)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            result.update(rsf.errors)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        rsf.save()
        result["msg"] = "更新成功"
        result["code"] = 0
        result["data"] = rsf.data
        return Response(result, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        # pk为指定删除对象的id
        result = {}
        res = self.pk_validity(pk)
        res.delete()
        result["msg"] = "删除成功"
        result["code"] = 0
        return Response(result, status=status.HTTP_204_NO_CONTENT)

    def pk_validity(self, pk):
        """
        用作效验pk传值参数
        :param pk:
        :param result:
        :return:
        """
        result = {}
        try:
            res = Interfaces.objects.get(id=pk)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            # return JsonResponse(result, status=400)
            # 直接Http404也可以
            raise Http404(result)
        return res


# 如果要实现过滤、查询、分页等功能，需要继承GenericAPIView
# a.GenericAPIView为APIView的子类，拓展了过滤、查询、分页
class InterfacesModelPage(GenericAPIView):
    # b.往往要指定queryset，当前接口中需要使用到的查询集（查询集对象）
    # c.往往要指定serializer_class，当前接口中需要使用到的序列化器类
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer

    # 安装 pip install django-filter
    # 需要和项目一样在setting中注册
    # 导入from django_filters.rest_framework import DjangoFilterBackend
    # filter_backends来指定使用的过滤引擎，如果多个过滤引擎，可以在列表中添加
    # filterset_fields来指定需要过滤的字段，字段要与模型类中的字段名一致
    # 为精确匹配
    # 也可以在全局settings.py配置文件中指定所用视图公用的过滤引擎,使用DEFAULT_FILTER_BACKENDS属性
    # 如果视图中未指定，那么会使用全局的过滤引擎，如果视图中有指定，那么会使用视图中指定的过滤引擎（优先级更高）

    # 可以在filter_backends中指定OrderingFilter来实现排序功能
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields = ['name', 'leader', 'id']
    filterset_fields = ('name',)
    # 在ordering_fields来指定需要排序的字段
    # 前端在过滤时，需要使用ordering作为key，具体的排序字段作为value
    # 默认使用升序过滤，如果要降序，可以在排序字段前使用减号（-）
    # ordering_fields = ['id', 'name']
    ordering_fields = ('name',)
    # 在视图中指定分页引擎类,优先级比全局指定要高
    pagination_class = MyPagination

    def get(self, request):
        result = {}
        try:
            # d.可以使用.get_queryset()方法，获取查询集对象，尽量不要直接使用self.queryset
            # res = self.get_queryset()
            # 过滤前端?后传入的name参数
            # name = request.query_params.get('name')
            # if name:
            #     res = res.filter(name = name)
            # one_obj = InterfacesModelSerializer(instance=res, many=True)
            # ProjectsModelSerializer(*args, **kwargs)
            # e.可以使用.get_serializer()方法，调用序列化器类，尽量不要直接使用self.serializer_class
            # 需要调用.filter_queryset()方法，需要传递一个查询集对象
            # 返回一个查询集
            res = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(res)
            if page is not None:
                one_obj = self.get_serializer(instance=page, many=True)
                return self.get_paginated_response(one_obj.data)
            # serializer_obj = self.serializer_class(instance=qs, many=True)
            # ProjectsModelSerializer(*args, **kwargs)
            # e.可以使用.get_serializer()方法，调用序列化器类，尽量不要直接使用self.serializer_class
            one_obj = self.get_serializer(instance=res, many=True)
            return Response(one_obj.data, status=status.HTTP_200_OK)
        except Exception as e:
            result["msg"] = "查询失败，指定ID不存在"
            result["code"] = 1
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        res = self.get_object()
        rsf = InterfacesModelSerializer(instance=res, data=request.data)
        # 在视图中抛出的异常，DRF会自动来处理
        # 直接将报错信息以json格式返回
        rsf.is_valid(raise_exception=True)
        rsf.save()
        return Response(rsf.data, status=status.HTTP_201_CREATED)


# a.可以先继承DRF中的Mixin拓展类
# b.然后在继承GenericAPIView
# c.ListModelMixin -> .list()方法：实现获取列表数据
# d.CreateModelMixin -> .create()方法：实现创建数据
class InterfacesView1(ListModelMixin, CreateModelMixin,GenericAPIView):
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('name',)
    ordering_fields = ('name',)
    pagination_class = MyPagination

    def get(self, request, *args, **kwargs):
        # ListModelMixin中的list方法
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # CreateModelMixin中的create方法
        return self.create(request, *args, **kwargs)


# e.RetrieveModelMixin -> .retrieve()方法：实现获取详情数据
# e.UpdateModelMixin -> .update()方法：实现更新数据
# e.DestroyModelMixin -> .destroy()方法：实现删除数据
class InterfacesView2(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,GenericAPIView):
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer

    def get(self, request, *args, **kwargs):
        # RetrieveModelMixin中的retrieve方法
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # UpdateModelMixin中的update方法
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # DestroyModelMixin的destroy方法
        return self.destroy(request, *args, **kwargs)
