from django.urls import path, re_path
from envs import views
from rest_framework.routers import DefaultRouter, SimpleRouter

# 定义路由对象
router = DefaultRouter()
# router = SimpleRouter()
router.register(r'envs', views.EnvsViewSet)
urlpatterns = []
# 将这个列表添加至urlpatterns
urlpatterns += router.urls
