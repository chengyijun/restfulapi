from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class MyPageNumberPagination(LimitOffsetPagination):
    # 默认数据量
    default_limit = 10
    # 最大数据量
    max_limit = 50
    # 数据量
    limit_query_param = 'limit'
    # 起始偏移位置
    offset_query_param = 'offset'

    def get_paginated_response(self, data):
        """
        overwrite 不要父类给的数据格式
        :param data:
        :return:
        """
        return Response(data)

    def get_offset(self, request):
        """
        overwrite 让起始偏移量 始终为0
        :param request:
        :return:
        """
        return 0
