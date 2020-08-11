from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Testsuits
from .serializers import TestsuitsModelSerializer


class TestsuitsViewSet(ModelViewSet):
    queryset = Testsuits.objects.all()
    serializer_class = TestsuitsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'name']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name': instance.name,
            'include': instance.include,
            'project_id': instance.project_id
        }
        return Response(data)