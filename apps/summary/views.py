from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response

from .serializers import SummaryModelSerializer
from projects.models import Projects
from interfaces.models import Interfaces
from testcases.models import Testcases
from testsuits.models import Testsuits
from configures.models import Configures
from envs.models import Envs
from debugtalks.models import DebugTalks
from reports.models import Reports


class SummaryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Reports.objects.all()
    serializer_class = SummaryModelSerializer

    def list(self, request, *args, **kwargs):
        # 取出并构造参数
        response = super().list(request, *args, **kwargs)
        result = response.data.get("results")
        user = User.objects.filter(is_staff=1)[0]
        projects_count = Projects.objects.all().count()
        interfaces_count = Interfaces.objects.all().count()
        testcases_count = Testcases.objects.all().count()
        testsuits_count = Testsuits.objects.all().count()
        configures_count = Configures.objects.all().count()
        envs_count = Envs.objects.all().count()
        debug_talks_count = DebugTalks.objects.all().count()
        reports_count = Reports.objects.all().count()
        success_rate = 0
        fail_rate = 0
        for item in result:
            counts = item.get("count")
            success_rate = item.get("success") + success_rate
            fail_rate = fail_rate + (counts - item.get("success"))

        data = {
            "user": {
                "username": user.username,
                "role": "管理员",
                "date_joined": user.date_joined,
                "last_login": user.last_login
            },
            "statistics": {
                "projects_count": projects_count,
                "interfaces_count": interfaces_count,
                "testcases_count": testcases_count,
                "testsuits_count": testsuits_count,
                "configures_count": configures_count,
                "envs_count": envs_count,
                "debug_talks_count": debug_talks_count,
                "reports_count": reports_count,
                "success_rate": success_rate,
                "fail_rate": fail_rate
            }
        }
        return Response(data)

    def get_serializer_class(self):
        return SummaryModelSerializer if self.action == 'list' else self.serializer_class
