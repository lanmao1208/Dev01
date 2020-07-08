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
        # 获取查询对象
        result = {"data":{}}
        try:
            # pk存在则为指定查询对象
            if pk:
                res = Interfaces.objects.values().filter(id=pk)
            # 不存在则为查询所有对象
            else:
                res = Interfaces.objects.values().all()
            result["data"] = list(res)
            result["msg"] = "查询成功"
            result["code"] = 0
            print(result)
            return JsonResponse(result, safe=False)
        except Exception as e:
            result["msg"] = "查询失败"
            result["code"] = 1
            return JsonResponse(result)

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


    def post(self, request):
        # json格式传入创建需要的参数
        create_data = json.loads(request.body)
        result = {}
        try:
            Interfaces.objects.create(**create_data)
            result["msg"] = "创建成功"
            result["code"] = 0
            return JsonResponse(result)
        except Exception as e:
            result["msg"] = "创建失败"
            result["code"] = 1
            return JsonResponse(result)

    def put(self, request, pk = None):
        # 更新id为pk，更新内容通过json传递
        updata_data = json.loads(request.body)
        result = {}
        try:
            if pk:
                res = Interfaces.objects.get(id = pk)
                res.name = updata_data.get("name",None) or res.name
                res.projects_id = updata_data.get("projects_id", None) or res.projects_id
                res.tester = updata_data.get("tester", None) or res.tester
                res.desc = updata_data.get("desc", None) or res.desc
                res.save()
                result["msg"] = "更新成功"
                result["code"] = 0
                return JsonResponse(result)
        except Exception as e:
            result["msg"] = "更新失败"
            result["code"] = 1
            return JsonResponse(result)

    def delete(self, request, pk = None):
        # pk为指定删除对象的id
        result = {}
        try:
            if pk:
                Interfaces.objects.filter(id = pk).delete()
                result["msg"] = "删除成功"
                result["code"] = 0
                return JsonResponse(result)
        except Exception as e:
            result["msg"] = "删除失败"
            result["code"] = 1
            return JsonResponse(result)
