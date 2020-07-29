import random
import uuid

from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Users
from api.myserializers.login import LoginSerializer


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
        phone = ser.validated_data.get('phone', None)
        # conn = get_redis_connection('default')
        # if not conn.get(phone, ):
        #     return Response({'status': 0,
        #                      'data': {
        #                          'token': '',
        #                          'phone': ''
        #                      },
        #                      'message': '验证码过期'
        #                      })
        # if conn.get(phone, ).decode('utf-8') != ser.validated_data.get('code', ):
        #     return Response({'status': 0,
        #                      'data': {
        #                          'token': '',
        #                          'phone': ''
        #                      },
        #                      'message': '验证码不正确'
        #                      })
        token = str(uuid.uuid4())

        # 登录成功 输入入库
        user, _ = Users.objects.get_or_create(phone=phone)
        nickname = request.data.get('nickname')
        avatar = request.data.get('avatar')

        user.token = token
        user.nickname = nickname
        user.avatar = avatar
        user.save()

        return Response({'status': 1,
                         'data': {
                             'token': token,
                             'phone': request.data.get('phone')
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
