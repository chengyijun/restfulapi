from django.urls import path

from testcelery.views import TestCelery, ResultCelery

app_name = 'testcelery'
urlpatterns = [
    # 执行触发celery task
    path('celery/', TestCelery.as_view(), name='celery'),
    # 查询celery task的执行结果
    path('result/', ResultCelery.as_view(), name='result'),

]
