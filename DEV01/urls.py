"""DEV01 URL Configuration

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
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Lemon API接口文档平台",  # 必传
#         default_version='v1',  # 必传
#         description="这是一个美轮美奂的接口文档",
#         terms_of_service="http://api.keyou.site",
#         contact=openapi.Contact(email="keyou@qq.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     # permission_classes=(permissions.AllowAny,),   # 权限类
# )
# 账户密码配置方法
# 在app项目的Terminal，输入python manage.py createsuperuser
# 会让你输入 username,email,password，依次输入。完成后再尝试登录swagger，输入刚才创建的user和password，即可登录成功。
urlpatterns = [
    path('admin/', admin.site.urls),
    # 添加接口文档平台的路由条目
    path('docs/', include_docs_urls(title='测试平台接口文档', description='xxx描述')),
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema- redoc'),
    # 类视图定义路由
    # a.path函数的第二个参数为类视图名.as_view()
    # b.可以使用<url类型转化器:路径参数名>
    # c.int、path、uuid、slug等等
    path('', include('debugtalks.urls')),
    path('', include('envs.urls')),
    path('', include('interfaces.urls')),
    path('', include('projects.urls')),
    path('', include('reports.urls')),
    path('', include('testcases.urls')),
    path('', include('testsuits.urls')),
    path('api/',include('rest_framework.urls')),
    path('user/',include('user.urls')),
]
