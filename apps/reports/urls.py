from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views


# 定义路由对象
router = DefaultRouter()
router.register(r'report', views.ReportsViewSet)
urlpatterns = []
urlpatterns += router.urls
