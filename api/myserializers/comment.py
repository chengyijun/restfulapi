from rest_framework import serializers

from api.models import Comments


class CommentSerializerForList(serializers.ModelSerializer):
    user__nickname = serializers.CharField(source='user.nickname', read_only=True)
    user__avatar = serializers.CharField(source='user.avatar', read_only=True)
    reply__user__nickname = serializers.CharField(source='reply.user.nickname', read_only=True)

    class Meta:
        model = Comments
        exclude = ['article', 'user', 'reply']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        exclude = []
