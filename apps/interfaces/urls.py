from interfaces import views
from rest_framework.routers import DefaultRouter, SimpleRouter

# 定义路由对象
router = DefaultRouter()
# router = SimpleRouter()
router.register(r'interfaces', views.InterfacesViewSet)
urlpatterns = []
# 将这个列表添加至urlpatterns
urlpatterns += router.urls
