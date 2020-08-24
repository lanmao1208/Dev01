from django.urls import path, re_path
from . import views
from rest_framework.routers import DefaultRouter

# 定义路由对象
router = DefaultRouter()
# router = SimpleRouter()
router.register(r'summary', views.SummaryViewSet)
urlpatterns = []
# 将这个列表添加至urlpatterns
urlpatterns += router.urls
