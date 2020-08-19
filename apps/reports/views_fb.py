import os
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.http.response import StreamingHttpResponse
from django.utils.encoding import escape_uri_path

from .models import Reports
from .serializers import ReportsModelSerializer
from .utils import get_file_content


class ReportsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id', 'name']

    # def list(self, request, *args, **kwargs):
    #     pass
    #
    # def retrieve(self, request, *args, **kwargs):
    #     pass

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # 获取html源码
        instance = self.get_object()
        html = instance.html
        name = instance.name

        # 获取测试报告所属目录路径
        report_dir = settings.REPORT_DIR

        # 生成html文件，存放到reports目录下
        report_full_dir = os.path.join(report_dir, name) + '.html'
        if not os.path.exists(report_full_dir):
            with open(report_full_dir, 'w', encoding='utf-8') as file:
                file.write(html)

        # 获取文件流，返回给前端
        # 创建一个生成器，获取文件流，每次获取的是文件字节数据

        response = StreamingHttpResponse(get_file_content(report_full_dir))

        html_file_name = escape_uri_path(name + '.html')
        # 添加响应头
        # 直接使用Response对象['响应头名称'] = '值'
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachement; filename*=UTF-8''{html_file_name}"

        # return StreamingHttpResponse(get_file_content(report_full_dir))
        return response
