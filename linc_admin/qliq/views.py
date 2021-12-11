import json
import os
import random

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import DatabaseError
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from common import util, apns, fcm
from common.error_code import *
from common.fcm import FCM_CARA, FCM_QLIQ
from qliq.models.apns_master import ApnsMaster


_FCM_MESSAGE = {
    'kr': {
        0: "밥은 먹었어요?",
        1: "잘 지내지요?",
        2: "오늘 하루 어땠어요?",
        3: "별일 없었어요?",
        4: "당신은 혼자가 아니랍니다.",
        5: "말 안해도 알아요. 많이 힘들었나봐요.",
        6: "커피 한잔 어때요?",
        7: "아, 바깥 바람 쐬니까 좋지요?",
        8: "우리 이제 산책이나 할까요?",
        9: "당신을 있는 그대로 사랑하세요.",
        10: "사랑한다. 마음을 열어보세요.",
        11: "제 손을 잡으세요.",
        12: "당신은 최고의 보물입니다.",
        13: "말해봐요. 잘 들어줄께요.",
        14: "시간이 빠르게 흐르네요.",
        15: "무슨 걱정 있어요?",
        16: "당신을 기다릴께요.",
        17: "밥은 먹었어요?",
        18: "당신을 생각하면 미소가 지어져요.",
        19: "속상해하지 마세요",
        20: "함께 힘내요!",
        21: "제가 도와줄께요.",
        22: "그냥 웃어봐요.",
        23: "젊어서 그런거예요.",
        24: "조금 더 기다려봐요.",
        25: "당당히 걸어봐요.",
    },
    'en': {
        0: "Have you eaten?",
        1: "How's it going?",
        2: "What a breezy day!",
        3: "How was your day?",
        4: "You're not alone.",
        5: "Fancy a coffee?",
        6: "Let's go for a walk.",
        7: "Love yourself for who you are.",
        8: "Open your mind to love.",
        9: "Hold my hand.",
        10: "Time flies.",
        11: "What's to worry about?",
        12: "I'll wait for you.",
        13: "Don't get upset.",
        14: "Go and see your love.",
        15: "Let me help you.",
        16: "Just smile.",
        17: "It's not a trouble.",
        18: "It's down to youth",
        19: "Just wait a little longer.",
        20: "Walk proudly.",
        21: "Whenever I think of you, I smile.",
        22: "You are better than you think.",
        23: "You want to go? Then let's go!",
        24: "Let's cheer up together!",
        25: "The most precious time is right now.",
    },
}


def normalize_phone_num(phone_num: str):
    phone_num = phone_num.replace(' ', '')
    phone_num = phone_num.replace('+82', '0')
    phone_num = phone_num.replace('+1', '')
    phone_num = phone_num.replace('+65', '')
    phone_num = phone_num.replace('+55', '')
    phone_num = phone_num.replace('+84', '0')
    phone_num = phone_num.replace('+44', '0')
    phone_num = phone_num.replace('+380', '')     # ua
    phone_num = phone_num.replace('+7', '')       # ru
    phone_num = phone_num.replace('-', '')

    return phone_num


# Create your views here.
@require_http_methods('POST')
def register(request):
    param = request.body_param

    did = param.get('apns_did', '')
    phone_num: str = param.get('apns_phone_num', '')
    os_type: str = param.get('apns_os_type', '')
    is_service: bool = param.get('is_service', False)
    phone_cc: str = param.get('apns_phone_cc', '')
    device_type: str = param.get('device_type', 'qliq')

    phone_num = normalize_phone_num(phone_num)

    rs = ApnsMaster.objects.filter(did=did, phone_num=phone_num)
    if phone_cc != '':
        rs = rs.filter(phone_cc=phone_cc)

    if len(rs) == 0:
        try:
            o = ApnsMaster()

            o.did = did
            o.phone_num = phone_num
            o.os_type = os_type
            o.is_service = is_service
            o.phone_cc = phone_cc
            o.device_type = device_type

            o.save()
        except DatabaseError:
            result = DB_ERROR
        else:
            result = 0
    else:
        result = 0

    return util.res_json(result)

@require_http_methods('POST')
def ya(request):
    param = request.body_param

    phone_num = param.get('apns_phone_num', '')
    location_url = param.get('ya_msg', '')
    sender_phone_num = param.get('sender', '')
    is_service = param.get('is_service', False)
    proc_date = param.get('proc_date', '')
    phone_cc = param.get('apns_phone_cc', '')

    phone_num = normalize_phone_num(phone_num)

    rs = ApnsMaster.objects.filter(phone_num=phone_num).order_by('-id')[0:1]
    if len(rs) == 0:
        return util.res_json(QLIQ_NO_PHONE_NUM)
    o = rs[0]

    # did 가 존재하지 않을 경우 아무것도 하지 않는다.
    if o.get_did() == '':
        pass
        # return util.res_json(QLIQ_NO_DID)

    if o.os_type == 'iOS':
        hey = f'Hey!\r\n{_FCM_MESSAGE.get(phone_cc, "en").get(random.randint(1, 25))}'
        print(hey)
        msg = f'{hey} from {sender_phone_num}'

        custom_data = {
            'id': '20',
            'value': hey,
            'temp': sender_phone_num,
            'date': proc_date,
        }
        apns.send(o.get_did(), 'qliq', ('dev', 'prd')[is_service], msg, 'hey_push.caf', custom_data)

        ret = ERROR_OK
    else:
        json_data = {
            'to': o.get_did(),
            'data': {
                'id': '20',
                'value': location_url,
                'temp': sender_phone_num,
                'date': proc_date,
            }
        }

        ret = fcm.send(json_data)

    return util.res_json(ret)


@require_http_methods('POST')
def sos(request, is_sos):
    param = request.body_param

    phone_num = param.get('apns_phone_num', '')
    location_url = param.get('location_url', '')
    sender_phone_num = param.get('sender', '')
    is_service = param.get('is_service', False)
    proc_date = param.get('proc_date', '')
    phone_cc = param.get('apns_phone_cc', '')
    sender_cust_no = param.get('sender_cust_no', '')
    altitude = param.get('altitude', '')

    phone_num = normalize_phone_num(phone_num)

    rs = ApnsMaster.objects.filter(phone_num=phone_num).order_by('-create_time')[0:1]
    if len(rs) == 0:
        return util.res_json(QLIQ_NO_PHONE_NUM)
    o = rs[0]

    # did 가 존재하지 않을 경우 아무것도 하지 않는다.
    if o.get_did() == '':
        pass
        # return util.res_json(QLIQ_NO_DID)

    if o.os_type == 'iOS':
        msg = (f"I'm here received. ({sender_phone_num})",
               f'SOS received. ({sender_phone_num})')[is_sos]

        custom_data = {
            'id': ('2', '3')[is_sos],
            'value': location_url,
            'temp': sender_phone_num,
            'date': proc_date,
            'custno': sender_cust_no,
            'altitude': altitude,
        }

        # qliq
        apns.send(o.get_did(), 'qliq', ('dev', 'prd')[is_service], msg, 'rang_push2.caf', custom_data)

        # rang TODO: 나중에 개발 + 인증서 갱신도 필요함.
        apns.send(o.get_did(), 'rang', ('dev', 'prd')[is_service], msg, 'rang_push2.caf', custom_data)

        ret = ERROR_OK
    else:
        json_data = {
            'to': o.get_did(),
            'data': {
                'id': ('2', '3')[is_sos],
                'value': location_url,
                'temp': sender_phone_num,
                'date': proc_date,
                'custno': sender_cust_no,
                'altitude': altitude,
            }
        }
        ret = fcm.send_all(json_data)

    return util.res_json(ret)


@require_http_methods('POST')
def sos_voice(request):
    param = request.body_param

    phone_num = param.get('apns_phone_num', '')
    voice = param.get('voice', '')
    sender_phone_num = param.get('sender', '')
    is_service = param.get('is_service', False)
    proc_date = param.get('proc_date', '')
    phone_cc = param.get('apns_phone_cc', '')
    sender_cust_no = param.get('sender_cust_no', '')
    picture_type = param.get('picture_type', False)

    phone_num = normalize_phone_num(phone_num)

    rs = ApnsMaster.objects.filter(phone_num=phone_num).order_by('-id')[0:1]
    if len(rs) == 0:
        return util.res_json(QLIQ_NO_PHONE_NUM)
    o = rs[0]

    # did 가 존재하지 않을 경우 아무것도 하지 않는다.
    if o.get_did() == '':
        pass
        # return util.res_json(QLIQ_NO_DID)

    # iOS 일 경우, 녹음이 되지 않아 아무 것도 할 수가 없다.
    if o.os_type == 'iOS':
        pass
    else:
        json_data = {
            'to': o.get_did(),
            'data': {
                'id': ('8', '6')[picture_type is True],
                'value': voice,
                'temp': sender_phone_num,
                'date': proc_date,
                'custno': sender_cust_no,
            }
        }
        fcm.send(json_data, FCM_QLIQ)
        fcm.send(json_data, FCM_CARA)

    return util.res_json()


@require_http_methods(['GET', 'POST'])
def sos_voice_upload(request):
    if request.method == 'GET':
        return render(request, 'qliq/sos_upload.html')

    # POST
    cust_no = request.POST.get('custNo', '0')

    if 'fileData' not in request.FILES:
        return util.res_json(PARAM_ERROR)

    sos_voice_file = request.FILES['fileData']
    if sos_voice_file:
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'qliq/sos/voice')
        file_name = f'{cust_no}.mp3'

        fs = FileSystemStorage(location=upload_dir)
        if fs.exists(file_name):
            fs.delete(file_name)
        file_path = fs.save(file_name, sos_voice_file)
        print(file_path)

    return util.res_json()
