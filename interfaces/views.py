from django.shortcuts import render

import json

# 0、导入HttpResponse
import datetime
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from interfaces.models import Interfaces
from django.db import connections

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
            return JsonResponse("<h2>GET请求：查询成功{}</h2>".format(res))
        except Exception as e:
            return JsonResponse("<h2>GET请求：该查询对象不存在</h2>")




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
                return JsonResponse("<h2>PUT请求：更新成功{}</h2>".format(Projects.objects.get(id=pk)), content_type='application/json', status=200)
        except Exception as e:
            return JsonResponse("<h2>PUT请求：更新失败，不存在该对象</h2>")

    def delete(self, request, pk = None):
        try:
            if pk:
                res = Interfaces.objects.filter(id = pk).delete()
                return JsonResponse("<h2>DELETE请求：删除成功</h2>")
        except Exception as e:
            return JsonResponse("<h2>DELETE请求：删除失败，不存在该对象</h2>")
