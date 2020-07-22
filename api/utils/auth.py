from rest_framework.authentication import BaseAuthentication

from api.models import Users


class MyGeneralAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        :param request:
        :return: None -表示本认证器不做任何处理直接交给下一个认证器 认证成功会返回一个元组  (user,token) 表示认证成功 并分贝绑定在
        request.user request.auth 属性上
        """
        # 获取token
        # 注意： 特别值得注意的是  前端 header = {
        #   'Authentication': 578fff92-e481-4223-a49a-427cdadfd915
        # }
        # drf框架中接收的时候   需要 加 HTTP_ 前缀 并将key全大写
        token = request.META.get('HTTP_AUTHENTICATION', None)
        # 如果token没有带过来
        if not token:
            return None
        # 如果token是错误的
        user = Users.objects.filter(token=token).first()
        if not user:
            return None
        # 通过认证  会返回一个元组（登录用户对象，登录用户token） 并将其作为request属性绑定上  使用的时候可以通过
        # request.user request.auth 拿到
        # print(user, token)
        return user, token
