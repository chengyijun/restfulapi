from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from api.models import Comments
from api.myserializers.comment import CommentSerializer, CommentSerializerForList
from api.utils.mypagination import MyPageNumberPagination


class CommentFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        root = request.query_params.get('root')
        article = request.query_params.get('article')
        # print(root, article)
        if root:
            queryset = queryset.filter(root=root, article=article).order_by('id')
        return queryset


class CommentView(ListAPIView, CreateAPIView):
    # 查询结果集
    queryset = Comments.objects.order_by('-id').all()
    # 自定义分页器
    pagination_class = MyPageNumberPagination
    # 自定义queryset结果集
    filter_backends = [CommentFilter]

    def get_serializer_class(self):
        # 根据不同请求 加载不同的序列化器
        if self.request.method == 'POST':
            return CommentSerializer
        elif self.request.method == 'GET':
            return CommentSerializerForList


class CommentDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    # 查询结果集
    queryset = Comments.objects.order_by('-id').all()
    # 序列化器类
    serializer_class = CommentSerializer
    lookup_field = 'id'

    # 自定义queryset结果集
    filter_backends = [CommentFilter]
