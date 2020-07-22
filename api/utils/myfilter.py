from rest_framework.filters import BaseFilterBackend


class MyBaseFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get('min_id')
        max_id = request.query_params.get('max_id')
        if min_id:
            # 处理上滑 翻页
            queryset = queryset.filter(id__lt=min_id).order_by('id')
        elif max_id:
            # 处理 下拉刷新
            queryset = queryset.filter(id__gt=max_id).order_by('id')
        else:
            queryset = queryset.order_by('id')
        return queryset
