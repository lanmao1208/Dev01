from django.urls import path, re_path
from testsuits import views
from rest_framework.routers import DefaultRouter, SimpleRouter

# 定义路由对象
router = DefaultRouter()
# router = SimpleRouter()
router.register(r'testsuits', views.TestsuitsViewSet)
urlpatterns = []
# 将这个列表添加至urlpatterns
urlpatterns += router.urls
