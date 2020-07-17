from interfaces.models import Interfaces
from .serializers import InterfacesModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from utils.pagination import MyPagination



class InterfacesViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('name',)
    ordering_fields = ('name',)
    pagination_class = MyPagination

