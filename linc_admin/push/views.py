# Create your views here.
import json

from django.views.decorators.http import require_http_methods
from django_redis import get_redis_connection

from common import util
from common.error_code import *
from device.models.swatch_user_info import SwatchUserInfo


@require_http_methods(["POST"])
def send_owner(request):
    param = json.loads(request.body)

    message = param.get('message', '').strip()
    target = param.get('target', [])

    if message == '':
        return util.res_json(PUSH_NO_MESSAGE)

    if len(target) == 0:
        return util.res_json(PUSH_NO_TARGET)

    try:
        target = [int(_) for _ in target]
    except:
        return util.res_json(PUSH_INVALID_TARGET)

    rs = SwatchUserInfo.objects.filter(id__in=target)
    for row in rs:
        push_message = make_push_message(row.is_android(), row.gcm_id, 3600, 'SAFEWATCH 알림', message)

        conn = get_redis_connection()
        conn.rpush('SAFEWATCH::GCM-PUSH', json.dumps(push_message, ensure_ascii=True))

    return util.res_json()



def make_push_message(is_android: bool, gcm_id: str, ttl: int, title: str, body: str):
    is_emergency = False

    message = {
        'content_available': True,
        'priority': 'high',
        'to': gcm_id,
        'data': {
            'event_type': 'TTS_MESSAGE',
        },
        'notification': None,
        'time_to_live': ttl,
    }

    notification = {
        'title': title,
        'body': body,
        'sound': ('default.wav', 'emergency.wav')[is_emergency]
    }

    if is_android:
        message['data'].update(notification)
        del message['notification']
    else:
        message['notification'] = notification

    return message
