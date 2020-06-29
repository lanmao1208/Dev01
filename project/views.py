from django.shortcuts import render

import json

# 0、导入HttpResponse
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render


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
        data = [
            {
                "project_name": "前程贷项目11",
                "leader": "可优",
                "app_name": "P2P平台应用"
            },
            {
                "project_name": "探索火星项目22",
                "leader": "优优",
                "app_name": "吊炸天应用"
            },
            {
                "project_name": "无比牛逼的项目33",
                "leader": "可可",
                "app_name": "神秘应用"
            },
        ]

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
        return JsonResponse(data, safe=False)

    def post(self, request, pk):
        # a.可以使用request.POST方法，去获取application/x-www-urlencoded类型的参数
        # b.可以使用request.body方法，去获取application/json类型的参数
        # c.可以使用request.META方法，获取请求头参数，key为HTTP_请求头key的大写
        data_dict = json.loads(request.body, encoding='utf-8')
        return HttpResponse("<h2>POST请求：欢迎{}！</h2>".format(data_dict['name']))

    def put(self, request, pk):
        # a.HttpResponse对象，第一个参数为字符串类型或者字节类型，会将字符串内容返回到前端
        # b.可以使用content_type来指定响应体的内容类型
        # c.可以使用status参数来指定响应状态码
        # return HttpResponse("<h2>PUT请求：欢迎测试开发测试的大佬们！</h2>")
        one_dict = '{"name": "keyou", "age": 18}'
        return HttpResponse(one_dict, content_type='application/json', status=201)

    def delete(self, request, pk):
        return HttpResponse("<h2>DELETE请求：欢迎测试开发测试的大佬们！</h2>")
