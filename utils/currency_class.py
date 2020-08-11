from rest_framework import viewsets


class Currency_View_Class(viewsets.ModelViewSet):

    # 封装视图中action动作的通用方法
    # 用于获取并覆盖response.data
    def currency_action_def(self, request, data_str, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data[data_str]
        return response
