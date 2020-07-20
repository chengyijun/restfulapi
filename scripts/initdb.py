import os
import random
import sys
import uuid

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miniprogramapi.settings")
import django

django.setup()

from api.models import Topics, Articles, Users, ArticleImages

# 新增用户
for _ in range(20):
    r = random.randint(111111111, 999999999)
    Users.objects.create(
        phone=f'13{r}',
        token=uuid.uuid4(),
        nickname=f'哨兵{r}号',
        avatar='http://himg.bdimg.com/sys/portrait/item/c9eee4b89ce69da5e4b89ce5be80e79a84e78caaa629.jpg'
    )

# 新增话题
for _ in range(20):
    r = random.randint(1, 200)
    Topics.objects.create(
        content=f"我是话题{r}",
        hot=r
    )

# 新增文章
for _ in range(20):
    r = random.randint(1, 200)
    Articles.objects.create(
        content=f"文章内容{r}",
        location=f"明珠路{r}",
        view_count=1,
        like_count=1,
        comment_count=1,
        topic=Topics.objects.get(id=random.choice([topic.id for topic in Topics.objects.all()])),
        user=Users.objects.get(id=random.choice([user.id for user in Users.objects.all()]))

    )

# 新增文章图片
for _ in range(40):
    r = random.randint(1, 200)
    ArticleImages.objects.create(
        cos_path='https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2846245393,3575188587&fm=26&gp=0.jpg',
        key=f'{r}.jpg',
        article=Articles.objects.get(id=random.choice([topic.id for topic in Articles.objects.all()])),
    )

# 新增浏览记录
# for _ in range(20):
#     r = random.randint(1, 200)
#     ViewRecords.objects.create(
#         article_id=random.choice([x for x in range(1, 20)]),
#         user_id=random.choice([x for x in range(1, 20)])
#     )

# 新增评论
# for _ in range(20):
#     r = random.randint(1, 200)
#     Comments.objects.create(
#         content=f"评论内容{r}",
#         reply=random.choice([x for x in range(1, 10)]),
#         depth=random.choice([1, 2, 3]),
#         root=random.choice([x for x in range(1, 10)]),
#         article_id=random.choice([x for x in range(1, 20)])
#
#     )
