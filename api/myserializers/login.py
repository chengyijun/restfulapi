import re

from rest_framework import serializers


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


class CodeValidator(object):
    def __call__(self, value, *args, **kwargs):
        if len(value) != 4:
            raise serializers.ValidationError('验证码长度必须为4位')


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[PasswordValidator()])
    code = serializers.CharField(label='验证码', validators=[CodeValidator()])
    nickname = serializers.CharField(label='昵称')
    avatar = serializers.CharField(label='用户图像')
