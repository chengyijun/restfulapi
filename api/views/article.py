from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from api.models import Articles
from api.myserializers.article import ArticleSerializer, ArticleSerializerForList
from api.utils.auth import MyGeneralAuthentication, MyLoginAuthentication
from api.utils.myfilter import MyBaseFilter
from api.utils.mypagination import MyPageNumberPagination


class ArticleView(CreateAPIView, ListAPIView):
    # 查询结果集
    queryset = Articles.objects.all()
    # 序列化器类
    # serializer_class = ArticleSerializer
    # 自定义分页器
    pagination_class = MyPageNumberPagination
    # 自定义queryset结果集
    filter_backends = [MyBaseFilter]

    def get_serializer_class(self):
        # 根据不同请求 加载不同的序列化器
        if self.request.method == 'POST':
            return ArticleSerializer
        elif self.request.method == 'GET':
            return ArticleSerializerForList

    # 钩子 重写该方法可以在 序列化完成 数据入库之前的时机  插入其他字段值
    def perform_create(self, serializer):
        print(serializer.initial_data)
        # userinfo_id = serializer.initial_data.get('user')
        # topic_id = serializer.initial_data.get('topic')
        # serializer.save() 方法的内部 又调用了 序列化器中的 create()方法
        article_obj = serializer.save(view_count=1, like_count=1, comment_count=1)
        return article_obj


class ArticleDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    # 查询结果集
    queryset = Articles.objects.all()
    # 序列化器类
    serializer_class = ArticleSerializerForList
    # django 默认的主键形参为pk 如果改用其他 应通过 lookup_field 显试指定出来
    lookup_field = 'id'

    # 指定登录认证器
    # authentication_classes = [MyGeneralAuthentication]

    def get_authenticators(self):
        # 根据不同请求 加载不同的认证中间件
        if self.request.method == 'POST':
            return [MyLoginAuthentication()]
        return [MyGeneralAuthentication()]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        print(111)
        # 此处验证是否登录  如果登录了 就可以更新浏览记录
        if not request.auth:
            return response

        print(222)
        # 检查是否浏览记录已经存在 不用再添加了
        # 拿到该文章所有的浏览记录
        id = kwargs.get('id')
        article = Articles.objects.filter(id=id).first()
        user = request.user
        print(article, user)
        if user in [u for u in article.viwers.all()]:
            return response

        # 向中间表添加数据  也就是浏览记录
        article.viwers.add(user)

        return response
