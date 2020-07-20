# Create your models here.
from django.db import models

"""
用户表
"""


class Users(models.Model):
    phone = models.CharField(verbose_name='手机号', max_length=11)
    token = models.CharField(verbose_name='用户token', max_length=64, null=True, blank=True)
    nickname = models.CharField(verbose_name='用户昵称', max_length=64, null=True, blank=True)
    avatar = models.CharField(verbose_name='用户头像', max_length=255, null=True, blank=True)


"""
话题表
"""


class Topics(models.Model):
    content = models.CharField(verbose_name='话题内容', max_length=255)
    hot = models.IntegerField(verbose_name='话题热度')


"""
文章里包含的图片表
"""


class ArticleImages(models.Model):
    cos_path = models.CharField(verbose_name='图片路径', max_length=255)
    key = models.CharField(verbose_name='图片名称key', max_length=255)
    article = models.ForeignKey(verbose_name='所属文章', to='Articles', on_delete=models.CASCADE, null=True, blank=True)


"""
文章表
"""


class Articles(models.Model):
    content = models.CharField(verbose_name='文章内容', max_length=255)
    location = models.CharField(verbose_name='地理位置', max_length=255)
    view_count = models.PositiveIntegerField(verbose_name='浏览数', default=0)
    like_count = models.PositiveIntegerField(verbose_name='点赞数', default=0)
    comment_count = models.PositiveIntegerField(verbose_name='评论数', default=0)

    # 外键
    topic = models.ForeignKey(verbose_name='所属话题', to='Topics', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(verbose_name='所属用户', to='Users', on_delete=models.CASCADE, null=True, blank=True)
    # 浏览记录 多对多
    viwers = models.ManyToManyField('Users', related_name='views')


"""
浏览记录表
"""

# class ViewRecords(models.Model):
#     # 外键
#     user = models.ForeignKey(verbose_name='所属用户', to='Users', on_delete=models.CASCADE, null=True, blank=True)
#     article = models.ForeignKey(verbose_name='所属文章', to='Articles', on_delete=models.CASCADE, null=True, blank=True)


"""
评论表
"""


class Comments(models.Model):
    content = models.CharField(verbose_name='评论内容', max_length=255)
    depth = models.IntegerField(verbose_name='评论级别')

    # 外键
    article = models.ForeignKey(verbose_name='所属文章', to='Articles', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(verbose_name='所属用户', to='Users', on_delete=models.CASCADE, null=True, blank=True)
    root = models.ForeignKey(verbose_name='所属根评论', to='self', related_name='roots', null=True, blank=True,
                             on_delete=models.CASCADE)
    reply = models.ForeignKey(verbose_name='上级评论', to='self', related_name='replys', null=True, blank=True,
                              on_delete=models.CASCADE)
