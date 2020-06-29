"""Dev01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project.views import index_page, index_page2, IndexPage

urlpatterns = [
    path('index/', index_page),
    path('index2/', index_page2),
    # 类视图定义路由
    # a.path函数的第二个参数为类视图名.as_view()
    # b.可以使用<url类型转化器:路径参数名>
    # c.int、path、uuid、slug等等
    # path('index3/<int:pk>/', IndexPage.as_view()),
    path('index3/', IndexPage.as_view()),

]