import json
import os
from datetime import datetime

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings

from .models import Testcases
from envs.models import Envs
from interfaces.models import Interfaces
from . import serializers
from utils import common,handle_datas



class TestcasesViewSet(ModelViewSet):
    queryset = Testcases.objects.all()
    serializer_class = serializers.TestcasesModelSerializer

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
        variables = [{"key": vkey, "value": vvalue,"param_type": handle_datas.handle_param_type(vvalue)}for vkey,vvalue in variables_item.items() if variables_item.items() is not None]
        # 处理用例variables变量列表
        globalVar_item = testcase_request.get('test').get('variables')
        globalVar = [{"key": list(item)[0], "value": item.get(list(item)[0]),
                      "param_type": handle_datas.handle_param_type(item.get(list(item)[0]))}
                     for item in globalVar_item if globalVar_item is not None]
        # 处理用例的validate列表
        validate_item = testcase_request.get('test').get('validate')
        validate = [{"key": item.get("check"), "value": item.get("expected"), "comparator": item.get("comparator"),
                     "param_type": handle_datas.handle_param_type(item.get("expected"))} for item in validate_item if
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

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        # 取出并构造参数
        instance = self.get_object()
        response = super().create(request, *args, **kwargs)
        env_id = response.data.serializer.validated_data.get('env_id')
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建一个以时间戳命名的路径
        os.makedirs(testcase_dir_path)
        env = Envs.objects.filter(id=env_id).first()
        # 生成yaml用例文件
        common.generate_testcase_file(instance, env, testcase_dir_path)
        # 运行用例（生成报告）
        common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        return serializers.TestcasesRunSerializer if self.action == 'run' else self.serializer_class

    def perform_create(self, serializer):
        # 重写父类的perform_create方法，使用run动作时不进行保存操作
        if self.action == 'run':
            pass
        else:
            serializer.save()