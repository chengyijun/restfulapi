from django.urls import path, re_path

from api.views.article import ArticleView, ArticleDetailView
from api.views.comment import CommentView, CommentDetailView
from api.views.cosauth import TempAuthView
from api.views.login import LoginView, CodeView
from api.views.topic import TopicView, TopicDetailView

app_name = 'aip'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('code/', CodeView.as_view(), name='code'),
    path('tempauth/', TempAuthView.as_view(), name='tempauth'),

    # APIView
    path('articles/', ArticleView.as_view(), name='articles'),
    # re_path(r'article/(?P<id>\d+)/$', ArticleDetailView.as_view(), name='article-detail'),
    # 等价于上面的写法
    path('article/<id>/', ArticleDetailView.as_view(), name='article-detail'),

    path('topics/', TopicView.as_view(), name='topics'),
    re_path(r'topic/(?P<id>\d+)/$', TopicDetailView.as_view(), name='article-detail'),

    path('comments/', CommentView.as_view(), name='comments'),
    re_path(r'comment/(?P<id>\d+)/$', CommentDetailView.as_view(), name='comment-detail'),

]
