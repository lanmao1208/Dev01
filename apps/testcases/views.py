import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Testcases
from interfaces.models import Interfaces
from .serializers import TestcasesModelSerializer


def handle_param_type(value):
    """
    处理参数类型
    :param value: 数据
    :return: value数据的类型名
    """
    if isinstance(value, int):
        param_type = "int"
    elif isinstance(value, float):
        param_type = "float"
    elif isinstance(value, bool):
        param_type = "boolean"
    else:
        param_type = "string"

    return param_type


class TestcasesViewSet(ModelViewSet):
    queryset = Testcases.objects.all()
    serializer_class = TestcasesModelSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        获取用例详情信息
        """
        # Testcase对象
        response = self.get_object()
        # 用例前置信息
        include = json.loads(response.include)
        # 用例请求信息
        testcase_request = json.loads(response.request)
        request_datas = testcase_request.get('test').get('request')
        # selected_configure_id
        testcase_configures_id = include.get("config")
        # selected_interface_id
        testcase_interface_id = response.interface_id
        # selected_project_id
        testcase_project_id = Interfaces.objects.filter(id=testcase_interface_id)[0].project_id
        testcase_id_list = include.get("testcases")
        # 处理用例的header列表
        headers_item = testcase_request.get("headers")
        headers = [{"key": hkey, "value": hvalue} for hkey, hvalue in headers_item if headers_item is not None]
        # 处理form表单数据
        variables_item = request_datas.get('data')
        variables = [{"key": vkey, "value": vvalue,"param_type": handle_param_type(vvalue)}for vkey,vvalue in variables_item.items() if variables_item.items() is not None]
        # 处理用例variables变量列表
        globalVar_item = testcase_request.get('test').get('variables')
        globalVar = [{"key": list(item)[0], "value": item.get(list(item)[0]),
                      "param_type": handle_param_type(item.get(list(item)[0]))}
                     for item in globalVar_item if globalVar_item is not None]
        # 处理用例的validate列表
        validate_item = testcase_request.get('test').get('validate')
        validate = [{"key": item.get("check"), "value": item.get("expected"), "comparator": item.get("comparator"),
                     "param_type": handle_param_type(item.get("expected"))} for item in validate_item if
                    validate_item is not None]
        # 处理extract数据
        extract_item = testcase_request.get('test').get('extract')
        extract = [{"key": list(item)[0], "value": str(item.get(list(item)[0]))} for item in extract_item if
                   extract_item is not None]
        # 处理用例的param数据
        param_item = testcase_request.get("test").get("param")
        param = [{"key": pkey, "value": pvalue} for pkey, pvalue in param_item if param_item is not None]
        # 处理parameters数据
        parmeterized_item = testcase_request.get('test').get('parameters')
        parmeterized = [{"key": list(item)[0], "value": str(item.get(list(item)[0]))} for item in parmeterized_item if
                        parmeterized_item is not None]
        # 处理setupHooks数据
        setupHooks_item = testcase_request.get('test').get('setup_hooks')
        setupHooks = [{"key": item} for item in setupHooks_item if setupHooks_item is not None]
        # 处理teardownHooks数据
        teardownHooks_item = testcase_request.get('test').get('teardown_hooks')
        teardownHooks = [{"key": item} for item in teardownHooks_item if teardownHooks_item is not None]
        # 处理json数据
        jsonVariable = json.dumps(request_datas.get('json'), ensure_ascii=False)

        datas = {
            "author": response.author,
            "testcase_name": response.name,
            "selected_configure_id": testcase_configures_id,
            "selected_interface_id": testcase_interface_id,
            "selected_project_id": testcase_project_id,
            "selected_testcase_id": testcase_id_list,

            "method": request_datas.get('method'),
            "url": request_datas.get('url'),
            "param": param,
            "header": headers,
            "variable": variables,  # form表单请求数据
            "jsonVariable": jsonVariable,

            "extract": extract,
            "validate": validate,
            "globalVar": globalVar,  # 变量
            "parameterized": parmeterized,
            "setupHooks": setupHooks,
            "teardownHooks": teardownHooks,
        }
        return Response(datas)
