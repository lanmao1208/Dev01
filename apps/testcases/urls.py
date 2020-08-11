from django.urls import path, re_path
from testcases import views
from rest_framework.routers import DefaultRouter, SimpleRouter

# 定义路由对象
router = DefaultRouter()
# router = SimpleRouter()
router.register(r'testcasess', views.TestcasesViewSet)
urlpatterns = []
# 将这个列表添加至urlpatterns
urlpatterns += router.urls
