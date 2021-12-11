import json
from json import JSONDecodeError

import requests

from common.error_code import *
from qliq.models.apns_master import ApnsMaster

FCM_QLIQ = 'qliq'
# FCM_SAFETY = 'qliq.safety'
FCM_RANG = 'rang'
FCM_CARA = 'cara'

_FCM_URL = 'https://fcm.googleapis.com/fcm/send'
_FCM_KEY = {
    # FCM_QLIQ: 'AIzaSyCyQDJNrvuctodbRFGSlSSuAEfNn7eDoI8',
    # FCM_SAFETY: 'AIzaSyBx8vyAbv2P9Oc9k54ZhEw9imhmTqy5Bys',
    # FCM_CARA: 'AIzaSyDGG22W6f9_BmpChCZmpOcq_LM9gTLwbyA',
    FCM_QLIQ: 'AAAAPbeVHlQ:APA91bFEaQkFmsGIQCPdWk6tW-zsLCKXhZzc6AJ_6dMIsd3yT8euVQMxXYc5FEg3cdUdNogVvU5I4Pa-wp1ku1B7A4OOsoB_vSwa9OCFD8sL0cGK3FJzTP6YAlW2iP7kOE18gkqs5K_x',
    FCM_RANG: 'AAAAf7lSfok:APA91bE8CD04Ar-F1k-sKZcoFRxYEBfwsfh7W19cBEMNc-kBZLb-ISkO2XQs_Eke5SekdIz5bfOlelYIXiCfZomNAtEEucVvStKXv_7UF93wkA7hP01GXUatOb7ZH_9hMPVzd4r61Qus',
    FCM_CARA: 'AAAAu9C5Apg:APA91bH6Re37cWnpqAqFVZuSqcrInMDVgL2ZMt79oIjst5i3Rb04WVSVua_OooUNqAKSyVK9_YCLoQtgltfVWik7tPXLhOLIHd1RdaZhEy7nJ9dcgFd9R8nHccru6gsG9g9rSAu1w19W',
}


def send(data: dict, app_type=FCM_QLIQ, do_feedback=True):
    conn = requests.Session()

    headers = {
        'Authorization': '='.join(['key', _FCM_KEY.get(app_type)])
    }

    print(f'@@@ {app_type} FCM REQ:', data)
    res = conn.post(_FCM_URL, json=data, headers=headers)
    if res.status_code == requests.codes.ok:
        print(f'### {app_type} FCM RES:', res.text)
        if do_feedback:
            try:
                js = json.loads(res.text)
            except JSONDecodeError:
                pass
            else:
                if js['success'] == 0 and js['failure'] == 1:
                    if js['results'][0]['error'] == 'NotRegistered':
                        ApnsMaster.clear_invalid_did(data.get('to'), app_type)

        return ERROR_OK
    else:
        print(res.status_code)
        return PUSH_ERROR


def send_all(data: dict, do_feedback=True):
    for app_type in _FCM_KEY.keys():
        send(data, app_type, do_feedback=True)

    return ERROR_OK
