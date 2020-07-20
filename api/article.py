from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.models import Article
from api.serializer import ArticleSerializer


class ArticleView(GenericAPIView):
    """列表视图"""
    # 查询结果集
    queryset = Article.objects.all()
    # 序列化器类
    serializer_class = ArticleSerializer

    def get(self, request):
        articles = self.get_queryset()

        serializer = self.get_serializer(articles, many=True)

        # 3.返回响应
        return Response(serializer.data)

    def post(self, request):
        # 1.获取参数
        data = request.data
        # 2.创建序列化器
        serializer = self.get_serializer(data=data)
        # 3.校验
        serializer.is_valid(raise_exception=True)
        # 4.保存
        serializer.save()
        # 5.返回响应
        return Response(serializer.data)


class ArticleDetailGenericAPIView(GenericAPIView):
    """详情视图"""

    # 查询结果集
    queryset = Article.objects.all()
    # 序列化器类
    serializer_class = ArticleSerializer

    # 默认是pk   修改后以下参数都要变
    lookup_field = 'id'

    def get(self, request, id):
        # 1.获取对象
        book = self.get_object()
        # 2.创建序列化器
        serializer = self.get_serializer(book)
        # 3.返回响应
        return Response(serializer.data)

    def put(self, request, id):
        # 1.获取对象
        book = self.get_object()
        # 2.接收参数
        data = request.data
        # 3.创建序列化器
        serializer = self.get_serializer(instance=book, data=data)
        # 4.验证
        serializer.is_valid(raise_exception=True)
        # 5.保存（更新）
        serializer.save()
        # 3.返回响应
        return Response(serializer.data)

    def delete(self, request, id):
        # 1.获取对象
        book = self.get_object()
        # 2.删除
        book.delete()
        # 3.返回响应
        return Response(status=status.HTTP_204_NO_CONTENT)
