import datetime
import json
from json import JSONDecodeError

from django.http import JsonResponse


class ElapseMiddleware:
    cnt = 0

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
        if request.content_type == 'application/json':
            try:
                setattr(request, 'body_param', json.loads(request.body, encoding='utf-8'))
            except JSONDecodeError:
                response = JsonResponse({
                    'error_code': -1,
                    'error_message': 'not json format',
                })
                response.status_code = 500

            print(f'REQ[{self.cnt:06d}]:', request.path, request.body)
        else:
            print(f'REQ[{self.cnt:06d}]:', request.path, request.content_type)
        if response is None:
            response = self.get_response(request)

        t2 = datetime.datetime.now()

        if type(response) is JsonResponse:
            print(f'RES[{request.COUNT:06d}]:', request.path, response.content.decode(), (t2 - t1).total_seconds())
        else:
            print(f'RES[{request.COUNT:06d}]:', request.path, (t2 - t1).total_seconds())

        # Code to be executed for each request/response after
        # the view is called.

        return response
