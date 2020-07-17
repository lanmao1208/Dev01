from django.urls import path
from interfaces import view_homework


urlpatterns = [
    path('interfaces/', view_homework.InterfacesModelPage.as_view()),
]