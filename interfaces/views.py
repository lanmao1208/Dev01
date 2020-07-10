import json
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from interfaces.models import Interfaces
from django.db import connections
from .serializers import InterfaceSerializer

"""
序列化器对象中的几个重要属性
一、一定要先执行.is_valid()方法之后才能访问
.errors 获取报错信息
.validated_data 校验通过之后的数据（往往也是数据库中需要保存的数据） 有可能不会过滤write_only

二、可以不用调用.is_valid()方法，也能访问
.data 最终返回给前端的数据
"""


class InterfacesPage(View):
    """
    类视图
    1、一定要继承View父类，或者View的子类
    2、可以定义get、post、put、delete方法，来分别实现GET请求、POST请求、PUT请求、DELETE请求
    3、get、post、put、delete方法名称固定，且均为小写
    4、实例方法的第二个参数为HttpRequest对象
    5、一定要返回HttpResponse对象或者HttpResponse子类对象
    """

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
        result = {"data": {}}
        try:
            # pk存在则为指定查询对象
            if pk:
                res = Interfaces.objects.filter(id=pk)
            # 不存在则为查询所有对象
            else:
                res = Interfaces.objects.all()
            one_obj = InterfaceSerializer(instance=res, many=True)
            result["data"] = one_obj.data
            result["msg"] = "查询成功"
            result["code"] = 0
            return JsonResponse(result, safe=False, status=201)
        except Exception as e:
            result["msg"] = "查询失败，指定ID不存在"
            result["code"] = 1
            return JsonResponse(result, status=400)

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
        # json格式传入创建需要的参数
        create_data = request.body
        result = {}
        # 判断传入参数是否为json或者字典格式
        try:
            # a.获取新的项目信息并转化为python中数据类型（字典或者嵌套字典的列表）
            create_json_data = json.loads(create_data)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            return JsonResponse(result, status=400)

        rsf = InterfaceSerializer(data=create_json_data)
        # 效验数据是否符合接口要求的参数设置
        try:
            # 创建序列化器对象
            rsf.is_valid(raise_exception=True)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            result.update(rsf.errors)
            return JsonResponse(result, status=400)
        # 效验通过后进行创建
        # c.创建项目,validated_data如果缺少某些字段，既不会报错也不会保存
        # Interfaces.objects.create(**rsf.validated_data)
        # 使用序列化器save方法，传递的关键字参数，会自动添加到create()方法，validated_data字典中
        # rsf.save(user = "创建人名字")
        rsf.save()
        result.update(rsf.data)
        result["msg"] = "创建成功"
        result["code"] = 0
        return JsonResponse(result, safe=False, status=201)

    def put(self, request, pk):
        result = {}
        # 更新id为pk，更新内容通过json传递
        try:
            res = Interfaces.objects.get(id=pk)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            return JsonResponse(result, status=400)
        # json格式传入创建需要的参数
        updata_data = request.body
        # 判断传入参数是否为json或者字典格式
        try:
            updata_json_data = json.loads(updata_data)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            return JsonResponse(result, status=400)
        # 如果在定义序列化器对象时，同时指定instance和data参数
        # a.调用序列化器对象.save()方法，会自动调用序列化器类中的update方法
        rsf = InterfaceSerializer(instance=res, data=updata_json_data)
        # 效验数据是否符合接口要求的参数设置
        try:
            rsf.is_valid(raise_exception=True)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            result.update(rsf.errors)
            return JsonResponse(result, status=400)
        rsf.save()
        result["msg"] = "更新成功"
        result["code"] = 0
        result["data"] = rsf.data
        return JsonResponse(result, status=201)

    def delete(self, request, pk):
        # pk为指定删除对象的id
        result = {}
        try:
            Interfaces.objects.filter(id=pk).delete()
            result["msg"] = "删除成功"
            result["code"] = 0
            return JsonResponse(result, status=201)
        except Exception as e:
            result["msg"] = "删除失败，查询不到指定id"
            result["code"] = 1
            return JsonResponse(result, status=400)
