from django.shortcuts import render

import json

# 0、导入HttpResponse
import datetime
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from projects.models import Projects
from django.db import connections
from interfaces import views

def index_page(request):
    """
    视图函数
    1、第一个参数为HttpRequest对象或者HttpRequest子类的对象，无需手动传递
    2、一般会使用request
    3、一定要返回HttpResponse对象或者HttpResponse子类对象
    :param request:
    :return:
    """
    if request.method == "GET":
        return HttpResponse("<h2>GET请求！</h2>")
    elif request.method == "POST":
        return HttpResponse("<h2>POST请求！</h2>")
    elif request.method == "PUT":
        return HttpResponse("<h2>POST请求！</h2>")


def index_page2(request):
    return HttpResponse("<h2>Hello！</h2>")


class IndexPage(View):
    """
    类视图
    1、一定要继承View父类，或者View的子类
    2、可以定义get、post、put、delete方法，来分别实现GET请求、POST请求、PUT请求、DELETE请求
    3、get、post、put、delete方法名称固定，且均为小写
    4、实例方法的第二个参数为HttpRequest对象
    5、一定要返回HttpResponse对象或者HttpResponse子类对象
    """
    def get(self, request):
        # 假设data数据是从数据库从读取的
        # a.render函数主要用于渲染模板生成一个html页面
        # b.第一个参数为request
        # b.第二个参数为在templates目录下的目录名
        # c.第三个参数为context，只能传字典
        # d.locals()函数能获取当前命名空间中的所有变量信息，然后存放在一个字典中
        # return render(request, 'demo.html')
        # return render(request, 'index.html', locals())
        # e.JsonResponse是HttpResponse的子类
        # 第一个参数为字典或者嵌套字典的列表，如果为非字典类型，需要将safe设置为False
        # 会返回一个json的字符串
        # 模型类对象方法
        res1 = Projects.objects.get(id = 1)
        # 第二种查询方法
        res = Projects.objects.filter(id__lte=4)
        return HttpResponse("<h2>GET请求：查询成功{}</h2>".format(res))


    def post(self, request):
        # a.可以使用request.POST方法，去获取application/x-www-urlencoded类型的参数
        # b.可以使用request.body方法，去获取application/json类型的参数
        # c.可以使用request.META方法，获取请求头参数，key为HTTP_请求头key的大写
        times = datetime.datetime
        # 模型类对象方法
        pro_one = Projects(name="django作业1{}".format(times),leader="负责人1{}".format(times),
                 tester="测试人员1{}".format(times),programmer="开发人员1{}".format(times))
        # 使用save()方法提交
        pro_one.save()
        # 创建方法二，使用查询集的Projects.objects.create()方法
        pro_two = Projects.objects.create(name="django作业2{}".format(times),leader="负责人2{}".format(times),
                 tester="测试人员2{}".format(times),programmer="开发人员2{}".format(times))
        return HttpResponse("<h2>POST请求：创建成功</h2>")

    def put(self, request):
        # a.HttpResponse对象，第一个参数为字符串类型或者字节类型，会将字符串内容返回到前端
        # b.可以使用content_type来指定响应体的内容类型
        # c.可以使用status参数来指定响应状态码
        # return HttpResponse("<h2>PUT请求：欢迎测试开发测试的大佬们！</h2>")
        # 获取id=1的数值，模型类对象方法
        res1 = Projects.objects.get(id=1)
        # 重新赋值
        res1.name = "修改后id1的name值"
        # 保存并提交
        res1.save()
        # 第二种更新方法
        res2 = Projects.objects.filter(id = 2).update(name = "修改后id2的name值")
        return HttpResponse("<h2>PUT请求：更新成功{}和{}</h2>".format(Projects.objects.get(id=1),
                                                              Projects.objects.get(id=2)), content_type='application/json', status=200)

    def delete(self, request):
        # 查询并删除，模型类对象方法
        res1 = Projects.objects.get(id=1)
        res1.delete()
        # 第二种删除方法
        res2 = Projects.objects.filter(id = 2).delete()
        return HttpResponse("<h2>DELETE请求：删除成功</h2>")

