# Create your views here.
import random
import re
import uuid

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from sts.sts import Sts

from api.models import Articles, Topics, Users
from api.serializer import ArticleSerializer, TopicSerializer, ArticleSerializerForList
from miniprogramapi import settings


class PasswordValidator(object):
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if len(value) != 11:
            raise serializers.ValidationError('手机号码长度不正确')
        if not re.match(r'^\d+$', value):
            raise serializers.ValidationError('手机号必须为数字')

    def set_context(self, serializer_field):
        # print(serializer_field)
        pass

    # def validate_phone(self, value):
    #     print(value + '``````````')
    #     raise serializers.ValidationError('aaaa')
    #     return value


class CodeValidator(object):
    def __call__(self, value, *args, **kwargs):
        if len(value) != 4:
            raise serializers.ValidationError('验证码长度必须为4位')


class LoginSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    phone = serializers.CharField(label='手机号', validators=[PasswordValidator()])
    code = serializers.CharField(label='验证码', validators=[CodeValidator()])

    # phone = serializers.CharField(label='手机号')


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            print(ser.errors)
            message_phone = dict(ser.errors).get('phone')[0] if dict(ser.errors).get('phone') else ''
            message_code = dict(ser.errors).get('code')[0] if dict(ser.errors).get('code') else ''
            message = message_phone + "\n" + message_code
            return Response({'status': 0,
                             'data': {
                                 'token': '',
                                 'phone': ''
                             },
                             'message': message
                             })
        # 数据验证通过 执行登录判断
        print(ser.validated_data)
        conn = get_redis_connection('default')
        phone = ser.validated_data.get('phone', )
        if not conn.get(phone, ):
            return Response({'status': 0,
                             'data': {
                                 'token': '',
                                 'phone': ''
                             },
                             'message': '验证码过期'
                             })
        if conn.get(phone, ).decode('utf-8') != ser.validated_data.get('code', ):
            return Response({'status': 0,
                             'data': {
                                 'token': '',
                                 'phone': ''
                             },
                             'message': '验证码不正确'
                             })
        token = str(uuid.uuid4())

        # 登录成功 输入入库
        user, _ = Users.objects.get_or_create(phone=phone)
        user.token = token
        user.save()

        return Response({'status': 1,
                         'data': {
                             'token': token,
                             'phone': request.data.get('phone', )
                         },
                         'message': '登录成功'
                         })


class CodeView(APIView):
    def get(self, request, *args, **kwargs):
        phone = request.query_params.dict().get('phone')
        seed_str = 'abcdefghjkmnpqrstuvwxy3456789'
        code = random.choices(seed_str, k=4)
        code_str = ''.join(code)
        print(code_str)
        # 得到验证码之后  存一份到redis(一分钟失效时间) 通过短信发走一份

        # conn = get_redis_connection('default')
        # conn.set(phone, code_str, 60)
        # TODO 通过短信发送一份验证码
        return Response({'status': 1,
                         'code': code_str})


class TempAuthView(APIView):
    def get(self, request, *args, **kwargs):
        config = {
            # 临时密钥有效时长，单位是秒
            'duration_seconds': 1800,
            'secret_id': settings.SecretId,
            # 固定密钥
            'secret_key': settings.SecretKey,
            # 设置网络代理
            # 'proxy': {
            #     'http': 'xx',
            #     'https': 'xx'
            # },
            # 换成你的 bucket
            'bucket': settings.Bucket,
            # 换成 bucket 所在地区
            'region': settings.Region,
            # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
            # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
            'allow_prefix': '*',
            # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
            'allow_actions': [
                # 简单上传
                'name/cos:PostObject',
                "name/cos:DeleteObject"
            ],

        }

        sts = Sts(config)
        response = sts.get_credential()
        return Response(response)


class ContentValidator(object):
    def __call__(self, value, *args, **kwargs):
        print('验证方法', value)


# def test(v):
#     print('rrrrr', v)


# class ArticleView(APIView):
#
#     def get(self, request):
#         # 1.获取所有书籍
#         articles = Article.objects.all()
#         # 2.通过序列化器的转换（模型转换为JSON）
#         serializer = ArticleSerializer(articles, many=True)
#         # 3.返回响应
#         return Response(serializer.data)
#
#     def post(self, request):
#         # 1.接收参数
#         data = request.data
#         # 2.验证参数（序列化器的校验）
#         print(data)
#         serializer = ArticleSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         # 3.数据入库
#         serializer.save()
#         # 4.返回响应
#         return Response(serializer.data)


from rest_framework.pagination import LimitOffsetPagination


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


class ArticleFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get('min_id')
        max_id = request.query_params.get('max_id')
        if min_id:
            # 处理上滑 翻页
            queryset = queryset.filter(id__lt=min_id).order_by('-id')
        elif max_id:
            # 处理 下拉刷新
            queryset = queryset.filter(id__gt=max_id).order_by('-id')
        else:
            queryset = queryset.order_by('-id')
        return queryset


class ArticleView(CreateAPIView, ListAPIView):
    # 查询结果集
    queryset = Articles.objects.all()
    # 序列化器类
    # serializer_class = ArticleSerializer
    # 自定义分页器
    pagination_class = MyPageNumberPagination
    # 自定义queryset结果集
    filter_backends = [ArticleFilter]

    def get_serializer_class(self):
        # 根据不同请求 加载不同的序列化器
        if self.request.method == 'POST':
            return ArticleSerializer
        elif self.request.method == 'GET':
            return ArticleSerializerForList

    # 钩子 重写该方法可以在 序列化完成 数据入库之前的时机  插入其他字段值
    def perform_create(self, serializer):
        print(serializer.initial_data)
        userinfo_id = serializer.initial_data.get('user')
        topic_id = serializer.initial_data.get('topic')
        # serializer.save() 方法的内部 又调用了 序列化器中的 create()方法
        article_obj = serializer.save(topic_id=topic_id, user_id=userinfo_id)
        return article_obj


class ArticleDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    # 查询结果集
    queryset = Articles.objects.all()
    # 序列化器类
    serializer_class = ArticleSerializerForList
    # django 默认的主键形参为pk 如果改用其他 应通过 lookup_field 显试指定出来
    lookup_field = 'id'


class TopicView(ListAPIView, CreateAPIView):
    # 查询结果集
    queryset = Topics.objects.order_by('-id').all()
    # 序列化器类
    serializer_class = TopicSerializer
    # 自定义分页器
    pagination_class = MyPageNumberPagination
    # 自定义queryset结果集
    filter_backends = [ArticleFilter]


class TopicDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    # 查询结果集
    queryset = Topics.objects.all()
    # 序列化器类
    serializer_class = TopicSerializer
    lookup_field = 'id'
