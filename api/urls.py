from django.urls import path, re_path

from api import views

app_name = 'aip'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('code/', views.CodeView.as_view(), name='code'),
    path('tempauth/', views.TempAuthView.as_view(), name='tempauth'),

    # APIView
    path('articles/', views.ArticleView.as_view(), name='articles'),
    # re_path(r'article/(?P<id>\d+)/$', views.ArticleDetailView.as_view(), name='article-detail'),
    # 等价于上面的写法
    path('article/<id>/', views.ArticleDetailView.as_view(), name='article-detail'),

    path('topics/', views.TopicView.as_view(), name='topics'),
    re_path(r'topic/(?P<id>\d+)/$', views.TopicDetailView.as_view(), name='article-detail'),

]
