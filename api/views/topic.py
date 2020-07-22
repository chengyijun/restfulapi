from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from api.models import Topics
from api.myserializers.topic import TopicSerializer
from api.utils.myfilter import MyBaseFilter
from api.utils.mypagination import MyPageNumberPagination


class TopicView(ListCreateAPIView):
    # 查询结果集
    queryset = Topics.objects.order_by('-id').all()
    # 序列化器类
    serializer_class = TopicSerializer
    # 自定义分页器
    pagination_class = MyPageNumberPagination
    # 自定义queryset结果集
    filter_backends = [MyBaseFilter]


class TopicDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    # 查询结果集
    queryset = Topics.objects.all()
    # 序列化器类
    serializer_class = TopicSerializer
    lookup_field = 'id'
