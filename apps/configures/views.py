import json
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Configures
from interfaces.models import Interfaces
from .serializers import ConfiguresModelSerializer
from utils import handle_datas


class ConfiguresViewSet(ModelViewSet):
    queryset = Configures.objects.all()
    serializer_class = ConfiguresModelSerializer

    def retrieve(self, request, *args, **kwargs):
        response = self.get_object()
        # 用例前置信息
        include = json.loads(response.include)
        # 用例请求信息
        testcase_request = json.loads(response.request)
        # selected_interface_id
        testcase_interface_id = response.interface_id
        # selected_project_id
        testcase_project_id = Interfaces.objects.filter(id=testcase_interface_id)[0].project_id
        # 处理用例的header列表
        headers_item = testcase_request.get("headers")
        headers = [{"key": hkey, "value": hvalue} for hkey, hvalue in headers_item if headers_item is not None]
        # 处理用例variables变量列表
        globalVar_item = testcase_request.get('test').get('variables')
        globalVar = [{"key": list(item)[0], "value": item.get(list(item)[0]),
                      "param_type": handle_datas.handle_param_type(item.get(list(item)[0]))}
                     for item in globalVar_item if globalVar_item is not None]

        results_datas = {
            "author": response.author,
            "configures_name": response.name,
            "selected_interface_id": testcase_interface_id,
            "selected_project_id": testcase_project_id,
            "header": headers,
            "globalVar": globalVar,
        }
        return Response(results_datas)
