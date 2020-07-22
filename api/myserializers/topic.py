from rest_framework import serializers

from api.models import Topics


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics  # 设置关联模型     model就是关联模型
        # fields = '__all__'  # fields设置字段   __all__表示所有字段
        # fields = ['content', 'location']
        exclude = []
