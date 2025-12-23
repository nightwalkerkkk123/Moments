from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # 每页默认10条数据
    page_size_query_param = 'pageSize'  # 前端可通过pageSize参数自定义每页条数
    page_query_param = 'page'  # 前端通过page参数指定页码
    max_page_size = 100  # 最大每页100条