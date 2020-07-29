# Create your views here.
from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework.views import APIView

from miniprogramapi import celery_app
from testcelery import tasks


class TestCelery(APIView):
    def get(self, request, *args, **kwargs):
        res = tasks.add.delay(1, 3)
        # 任务逻辑
        data = {'status': 'successful', 'task_id': res.task_id}
        return Response(data)


class ResultCelery(APIView):
    def get(self, request, *args, **kwargs):
        result_id = request.query_params.dict().get('result_id')
        # result_id = '1f9b12da-f4da-4562-a6d1-ad2d7e18d86b'
        result_obj = AsyncResult(id=result_id, app=celery_app)
        data = {
            'status': 1,
            'state': result_obj.state,
            'result': result_obj.get()
        }
        return Response(data)
