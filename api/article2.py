# ListModelMixin        获取全部对象（列表）
# CreateModelMixin      新增资源
# RetrieveModelMixin    获取一个资源
# UpdateModelMixin      更新一个资源
# DestroyModelMixin     删除一个资源
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

from api.models import Article
from api.serializer import ArticleSerializer


class ArticleListGenericMixinAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # 查询结果集
    queryset = Article.objects.all()
    # 序列化器类
    serializer_class = ArticleSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class ArticleDetailGenericMixinAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    # 查询结果集
    queryset = Article.objects.all()
    # 序列化器类
    serializer_class = ArticleSerializer

    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id)

    def put(self, request, id):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)
