from django.urls import path, re_path

# from projects.views import
from interfaces import views


urlpatterns = [
    path('interfaces/', views.InterfacesPage.as_view()),
    path('interfaces/<int:pk>/', views.InterfacesPage.as_view()),

]