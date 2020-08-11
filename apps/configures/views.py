from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Configures
from .serializers import ConfiguresModelSerializer


class ConfiguresViewSet(ModelViewSet):
    queryset = Configures.objects.all()
    serializer_class = ConfiguresModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'name']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name': instance.name,
            'project_id': instance.project_id,
            'include': instance.include
        }
        return Response(data)
