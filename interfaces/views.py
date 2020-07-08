import json
from django.http import  JsonResponse
from django.views import View
from django.shortcuts import render
from interfaces.models import Interfaces
from django.db import connections
from .serializers import InterfaceSerializer

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
                res = Interfaces.objects.filter(id=pk)
            # 不存在则为查询所有对象
            else:
                res = Interfaces.objects.all()
            one_obj = InterfaceSerializer(instance=res,many=True)
            result["data"] = one_obj.data
            result["msg"] = "查询成功"
            result["code"] = 0
            return JsonResponse(result,safe=False)
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
        create_data = request.body
        result = {}
        # 判断传入参数是否为json或者字典格式
        try:
            create_json_data = json.loads(create_data)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            return JsonResponse(result,status=400)

        rsf = InterfaceSerializer(data=create_json_data)
        # 效验数据是否符合接口要求的参数设置
        try:
            rsf.is_valid(raise_exception=True)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            result.update(rsf.errors)
            return JsonResponse(result,status=400)
        # 效验通过后进行创建
        Interfaces.objects.create(**rsf.validated_data)
        result.update(rsf.validated_data)
        result["msg"] = "创建成功"
        result["code"] = 0
        return JsonResponse(result, safe=False,status=200)

    def put(self, request, pk):
        # 更新id为pk，更新内容通过json传递
        # json格式传入创建需要的参数
        updata_data = request.body
        result = {}
        # 判断传入参数是否为json或者字典格式
        try:
            updata_json_data = json.loads(updata_data)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            return JsonResponse(result,status=400)

        rsf = InterfaceSerializer(data=updata_json_data)
        # 效验数据是否符合接口要求的参数设置
        try:
            rsf.is_valid(raise_exception=True)
        except Exception as e:
            result["msg"] = "参数错误"
            result["code"] = 1
            result.update(rsf.errors)
            return JsonResponse(result, status=400)
        # 效验通过后进行更新
        res = Interfaces.objects.get(id = pk)
        res.name = rsf.validated_data.get("name",None) or res.name
        res.projects_id = rsf.validated_data.get("projects_id", None) or res.projects_id
        res.tester = rsf.validated_data.get("tester", None) or res.tester
        res.desc = rsf.validated_data.get("desc", None) or res.desc
        res.save()
        result["msg"] = "更新成功"
        result["code"] = 0
        return JsonResponse(result,status=200)

    def delete(self, request, pk):
        # pk为指定删除对象的id
        result = {}
        try:
            Interfaces.objects.filter(id = pk).delete()
            result["msg"] = "删除成功"
            result["code"] = 0
            return JsonResponse(result)
        except Exception as e:
            result["msg"] = "删除失败"
            result["code"] = 1
            return JsonResponse(result)
