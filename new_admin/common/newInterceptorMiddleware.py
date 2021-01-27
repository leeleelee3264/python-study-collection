import datetime
import json
import logging

from json import JSONDecodeError
from django.http import JsonResponse

from common.error_code import *
from common.error_message import get_error_message

logger = logging.getLogger()


class Interceptor:
    cnt = 0
    # 다른 페이지 다 블락하고 로그인만 집어 넣을 수도 있다
    allow_path = []

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.cnt += 1
        request.COUNT = self.cnt
        t1 = datetime.datetime.now()

        response = None
        session_key = request.headers.get('Authorization', '')


        # TODO: 제외할 페스 넣어줬으면 사이즈 감별 지우기
        if not session_key and len(self.allow_path) > 0:
            if request.path not in self.allow_path:
                response = JsonResponse({
                    'result': False,
                    'result_code': ERROR_NO_SESSION_KEY,
                    'result_message': get_error_message(ERROR_NO_SESSION_KEY),
                })
        elif request.content_type == 'application/json' or request.content_type == 'text/plain':
            try:
                setattr(request, 'body_param', json.loads(request.body, encoding='utf-8'))
            except JSONDecodeError:
                # get 을 application/json 과 text/plain 둘 다 받기 위해
                if request.content_type == 'application/json' or request.content_type == 'text/plain':
                    pass
                else:
                    response = JsonResponse({
                        'result': False,
                        'result_code': ERROR_INVALID_PARAM_TYPE,
                        'result_message': get_error_message(ERROR_INVALID_PARAM_TYPE),
                    })
                    response.status_code = 200

            print(f'### REQ[{self.cnt:06d}]:', request.path, request.body)
        else:
            print(f'### REQ[{self.cnt:06d}]:', request.path, request.content_type)
        if response is None:
            response = self.get_response(request)

        if response.status_code == 404 and type(response) is not JsonResponse:
            response = JsonResponse({
                'result': False,
                'result_code': ERROR_INVALID_URL,
                'result_message': get_error_message(ERROR_INVALID_URL),
            })
        elif response.status_code == 500 and type(response) is not JsonResponse:
            response = JsonResponse({
                'result': False,
                'result_code': ERROR_SERVER_INTERNAL,
                'result_message': get_error_message(ERROR_SERVER_INTERNAL),
            })
        elif response.status_code == 405 and type(response) is not JsonResponse:
            response = JsonResponse({
                'result': False,
                'result_code': ERROR_NOT_SUPPORTED_METHOD,
                'result_message': get_error_message(ERROR_NOT_SUPPORTED_METHOD),
            })

        t2 = datetime.datetime.now()

        if type(response) is JsonResponse:
            print(f'### RES[{request.COUNT:06d}]:', request.path, response.content.decode(), (t2 - t1).total_seconds())
        else:
            print(f'### RES[{request.COUNT:06d}]:', request.path, (t2 - t1).total_seconds())

        # Code to be executed for each request/response after
        # the view is called.

        return response
