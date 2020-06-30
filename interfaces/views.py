from django.shortcuts import render

import json

# 0、导入HttpResponse
import datetime
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from interfaces.models import Interfaces
from django.db import connections
from django.db.models import Q

class InterfacesPage(View):
    """
    类视图
    1、一定要继承View父类，或者View的子类
    2、可以定义get、post、put、delete方法，来分别实现GET请求、POST请求、PUT请求、DELETE请求
    3、get、post、put、delete方法名称固定，且均为小写
    4、实例方法的第二个参数为HttpRequest对象
    5、一定要返回HttpResponse对象或者HttpResponse子类对象
    """

    def get(self, request, pk = None):
        # 获取所有查询对象
        try:
            if pk:
                res = Interfaces.objects.filter(id=pk)
            else:
                res = Interfaces.objects.all()
            res = list(res)
            print(res)
            return HttpResponse("{}".format(res))
        except Exception as e:
            return HttpResponse("<h2>GET请求：该查询对象不存在</h2>")

        # 关联查询
        # 通过从表信息获取父表信息
        # 从表模型类小名__从表字段名__查询表达式
        # 查询集对象，只有使用的时候才进行查询操作（惰性查找）
        # qs = Interfaces.objects.filter(interfaces__name__regex='^[0-9]')
        # 逻辑关系查询
        # 支持链式查询，可以使用多个filter方法进行过滤
        # 同一行查询中的多个条件是与的关系
        # qs =Interfaces.objects.filter(name__startswith="人").filter(programmer__contains="4")
        # qs =Interfaces.objects.filter(name__startswith="人",programmer__contains="4")
        # 同一行查询中的多个条件是或的关系
        # Q(条件)|Q(条件)...
        # qs = Interfaces.objects.filter(Q(leader__contains) | Q(programmer_contains = "4"))
        # 特殊操作
        # 根据name属性进行排序，不带“-”升序，带“-”降序
        # Interfaces.objects.all().order_by('-name')


    def post(self, request, pk = None):
        times = datetime.datetime
        try:
            Interfaces.objects.create(name="django作业2{}".format(times),leader="负责人2{}".format(times),
                 tester="测试人员2{}".format(times),programmer="开发人员2{}".format(times))
            return JsonResponse("<h2>POST请求：创建成功</h2>")
        except Exception as e:
            return JsonResponse("<h2>POST请求：创建失败</h2>")

    def put(self, request, pk = None):
        try:
            if pk:
                Interfaces.objects.filter(id = pk).update(name = "修改后id2的name值")
                return JsonResponse("<h2>PUT请求：更新成功{}</h2>".format(Interfaces.objects.get(id=pk)), content_type='application/json', status=200)
        except Exception as e:
            return JsonResponse("<h2>PUT请求：更新失败，不存在该对象</h2>")

    def delete(self, request, pk = None):
        try:
            if pk:
                res = Interfaces.objects.filter(id = pk).delete()
                return JsonResponse("<h2>DELETE请求：删除成功</h2>")
        except Exception as e:
            return JsonResponse("<h2>DELETE请求：删除失败，不存在该对象</h2>")
