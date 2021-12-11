from django.db import DatabaseError
from django.views.decorators.http import require_http_methods

from common import util, apns, fcm
from common.error_code import *
from qliq.models.apns_master import ApnsMaster
from qliq.views import normalize_phone_num


# Create your views here.
@require_http_methods('POST')
def register(request):
    param = request.body_param

    did = param.get('apns_did', '')
    phone_num: str = param.get('apns_phone_num', '')
    os_type: str = param.get('apns_os_type', '')
    is_service: bool = param.get('is_service', False)
    phone_cc: str = param.get('apns_phone_cc', '')
    device_type: str = param.get('device_type', 'rang')

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
