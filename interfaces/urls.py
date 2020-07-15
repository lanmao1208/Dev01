from django.urls import path, re_path
from interfaces import views


urlpatterns = [
    path('interfaces/', views.InterfacesPage.as_view()),
    path('interfaces/<int:pk>/', views.InterfacesPage.as_view()),
    path('InterfacesModelPage/',views.InterfacesModelPage.as_view()),
    # path('InterfacesModelPage/<int:pk>/',views.InterfacesModelPage.as_view())
]