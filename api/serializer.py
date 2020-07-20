from django.db.models import Max
from django.forms import model_to_dict
from rest_framework import serializers

from api.models import Articles, Topics, ArticleImages, Comments


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics  # 设置关联模型     model就是关联模型
        # fields = '__all__'  # fields设置字段   __all__表示所有字段
        # fields = ['content', 'location']
        exclude = []


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImages  # 设置关联模型     model就是关联模型
        # fields = '__all__'  # fields设置字段   __all__表示所有字段
        exclude = []


class ArticleSerializerForList(serializers.ModelSerializer):
    class Meta:
        model = Articles
        exclude = []

    topic = serializers.SerializerMethodField(label='所属话题', default='默认话题内容...', read_only=True)
    user = serializers.SerializerMethodField(label='所属用户手机号', default='13333333333', read_only=True)
    images = serializers.SerializerMethodField(label='文章包含的图片', default='', read_only=True)
    comments = serializers.SerializerMethodField(label='文章包含的评论', default='', read_only=True)

    def get_comments(self, value):

        # 统计文章评论数
        comment_count = value.comments_set.count()
        value.comment_count = comment_count

        # 统计该文章的一级评论
        comments_1 = value.comments_set.filter(depth=1).values('id')
        res = value.comments_set.filter(depth=1)

        # 统计该文章各一级评论之下的最新一条二级评论
        comments_2 = value.comments_set.filter(depth=2, reply__in=comments_1.all()).values('reply_id').annotate(
            max_id=Max('id'))
        child_ids = [s.get('max_id') for s in comments_2]
        res2 = Comments.objects.filter(id__in=child_ids)
        # 重新组装结果  将二级评论作为一级评论的child返回
        res3 = [r for r in res.values('id', 'content', 'user__nickname', 'user__avatar')]
        res2 = [r for r in res2.values('id', 'content', 'reply_id', 'user__nickname', 'user__avatar')]

        for x in res3:
            for y in res2:
                if x['id'] == y['reply_id']:
                    x['child'] = y

        return res3

    def get_images(self, value):
        images = value.articleimages_set.values('cos_path', 'key')
        return images

    def get_topic(self, value):
        topic = value.topic
        return model_to_dict(instance=topic)

    def get_user(self, value):
        user = value.user
        return model_to_dict(instance=user)


class ArticleSerializer(serializers.ModelSerializer):
    images = ArticleImageSerializer(many=True)

    class Meta:
        model = Articles  # 设置关联模型     model就是关联模型
        # fields = '__all__'  # fields设置字段   __all__表示所有字段
        # fields = ['content', 'location']
        # 排除的字段  直接丢弃  不验证 不入库
        exclude = ['topic', 'user']
        # exclude = []

    def create(self, validated_data):
        images = validated_data.pop('images')
        article_obj = Articles.objects.create(**validated_data)

        # Mark bulk_create() 方法 批量创建之后 返回的对象中 pk为None 可能是个框架bug
        # images_obj = ArticleImages.objects.bulk_create(
        #     [ArticleImages(**image, article=article_obj) for image in images])
        #
        # for o in images_obj:
        #     print('###', o.id)

        images_obj = [ArticleImages.objects.create(**image, article=article_obj) for image in images]
        article_obj.images = images_obj
        return article_obj

    # 验证字段 钩子
    # def validate_content(self, value):
    #     """ 验证是否还正在拍卖"""
    #     print('正在验证', value)
    #     # item_id = self.initial_data.get('item')
    #     # exists = models.AuctionItem.objects.filter(id=item_id, status=3).exists()
    #     # if not exists:
    #     #     raise exceptions.ValidationError('拍卖商品不存在或已成交')
    #     return value
