import locale
import json
import yaml
import os
from datetime import datetime

from rest_framework.response import Response
from rest_framework import serializers
from httprunner.task import HttpRunner
from httprunner.report import render_html_report

from debugtalks.models import DebugTalks
from configures.models import Configures
from testcases.models import Testcases
from reports.models import Reports


def create_report(runner, report_name=None):
    """
    生成报告方法
    :param runner:
    :param html_report_name:
    :param html_report_template:
    :return:
    """
    # 格式化时间轴
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary["time"]["start_datetime"] = start_datetime
    # duration保留三位数
    runner.summary["time"]["duration"] = round(runner.summary["time"]["duration"], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary["html_report_name"] = report_name

    for item in runner.summary["datails"]:
        try:
            for record in item["record"]:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content'].decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])
                request_body = record['meta_data']['response']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['response']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue
    summary = json.dump(runner.summary, ensure_ascii=False)

    report_name = report_name + "_" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    report_path = runner.gen_html_report(html_report_name = report_name)

    with open(report_path,encoding='utf-8') as f:
        reports = f.read()

    test_report = {
        'name':report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('success'),
        'conut': runner.summary.get('stat').get('testsRun'),
        'html':reports,
        'summary':summary
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj.id

def datetime_fmt():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    return '%Y年%m月%d日 %H:%M:%S'


def generate_testcase_file(instance, env, testcase_dir_path):
    """
    生成yaml用例文件
    :param instance:
    :param env:
    :param testcase_dir_path:
    :return:
    """
    testcase_list = []
    # 使用固定格式空白参数进行列表占位
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcase_list.append(config)

    # 获取include信息
    include = json.loads(instance.include, encoding='utf-8')
    # 获取request字段
    request = json.loads(instance.request, encoding='utf-8')
    # 获取用例所属接口名称
    interface_name = instance.interface.name
    # 获取用例所属项目名称
    project_name = instance.interface.project.name

    testcase_dir_path = os.path.join(testcase_dir_path, project_name)

    if not os.path.exists(testcase_dir_path):
        # 如果项目路径不存在，则创建项目路径
        os.makedirs(testcase_dir_path)
        # 创建debugTalk.py文件
        debugTalk_obj = DebugTalks.objects.filter(project__name=project_name).first()
        debugtalk = debugTalk_obj.debugtalk if debugTalk_obj else ""
        with open(os.path.join(testcase_dir_path, "debugtalk.py"), "w", encoding="utf-8") as f:
            f.write(debugtalk)
    # 接口文件路径
    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    if not os.path.exists(testcase_dir_path):
        # 如果项目路径不存在，则创建项目路径
        os.makedirs(testcase_dir_path)
    # 进行config数据效验
    if "config" in include:
        config_id = include.get("config")
        config_obj = Configures.objects.first(id=config_id).first()
        if config_obj:
            try:
                config_request = json.loads(config_obj.request, encoding="utf-8")
            except Exception as e:
                pass
                # raise serializers.ValidationError('request格式不正确')
            else:
                config_request["config"]["request"]["base_url"] = env.base_url if env else ''
                # 覆盖之前写的空白格式参数
                testcase_list[0] = config_request

    # 处理前置用例
    if "testcases" in include:
        testcase = include.get("testcases")
        # 避免接口写入数据问题，进行二次效验
        if testcase:
            for testcase_id in testcase:
                testcases_obj = Testcases.objects.filter(id=testcase_id).first()
                try:
                    testcases_request = json.loads(testcases_obj.request, encoding="utf-8")
                except Exception as e:
                    continue
                testcase_list.append(testcases_request)
    testcase_list.append(request)
    # 生成yaml文件
    with open(os.path.join(testcase_dir_path, instance.name + ".yaml"), "w", encoding="utf-8") as f:
        # 转换成yaml格式参数
        yaml.dump(testcase_list, f, allow_unicode=True)
        # f.write(yaml_data)


def run_testcase(instance, testcase_dir_path):
    # 运行函数
    runner = HttpRunner()
    try:
        runner.run(testcase_dir_path)
    except Exception as e:
        res = {
            "ret": False,
            "msg": "用例执行失败",
            "log": e
        }
        return Response(res, status=400)
    # 生成报告获取报告id
    report_id = create_report(runner, instance.name)
    # 用例运行完毕后返回报告id
    data = {
        "id": report_id
    }
    return Response(data, status=201)
