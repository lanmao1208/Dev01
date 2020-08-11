from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DebugTalks
from .serializers import DebugTalksModelSerializer


class DebugTalksViewSet(ModelViewSet):
    queryset = DebugTalks.objects.all()
    serializer_class = DebugTalksModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'project_id']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data_dict = {
            "id": instance.id,
            "debugtalks": instance.debugtalks
        }
        return Response(data_dict)
