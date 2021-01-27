"""
API response formatter
"""
from django.http import JsonResponse
from common.error_message import get_error_message


def res_json(error_code=0, data=None):
    result = {
        'code': error_code,
        'message': get_error_message(error_code)
    }

    if data is not None:
        result['data'] = data

    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

