from django.urls import path, re_path
from interfaces import views,views_bf


urlpatterns = [
    path('interfaces/', views_bf.InterfacesPage.as_view()),
    path('interfaces/<int:pk>/', views_bf.InterfacesPage.as_view()),
    # a.继承ViewSet之后，支持在定义路由时指定请求方法与action的映射
    # b.as_view需要接收一个字典
    # c.key为请求方法名，value为指定需要调用的action
    path('InterfacesViewSet/', views.InterfacesViewSet.as_view({
        'get': 'list',
        'post': 'create'
        })),
    path('InterfacesViewSet/<int:pk>/',views.InterfacesViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
        }))
]