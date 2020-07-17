from rest_framework.pagination import PageNumberPagination


# 重写PageNumberPagination父类，对分页进行拓展
class MyPagination(PageNumberPagination):
    # 指定默认每一页的数据条数
    page_size = 4
    # 设置前端指定页码的查询字符串key名称
    page_query_param = 'p'

    # 设置前端指定每一页数据条数的查询字符串key名称
    # 指定显示指定之后，前端才支持指定每一页的数据条数
    page_size_query_param = 's'
    # 指定最大的每一页的数据条数
    max_page_size = 50
