from django.urls import path, re_path

# from projects.views import
from projects import views


urlpatterns = [
    path('projects/', views.IndexPage.as_view()),
    path('projects/<int:pk>/', views.IndexPage.as_view()),

]