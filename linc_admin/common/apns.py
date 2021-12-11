import os

from common.apns_python.client import Client
from common.apns_python.notification import APS, Payload, Headers

from proj.settings.base import BASE_DIR

_CERT_PATH = {
    'qliq': {
        'dev': os.path.join(BASE_DIR, 'conf/qliq_dev.p12'),
        'prd': os.path.join(BASE_DIR, 'conf/qliq_prod.p12'),
    },
    'rang': {
        'dev': os.path.join(BASE_DIR, 'conf/rang_dev.p12'),
        'prd': os.path.join(BASE_DIR, 'conf/rang_prod.p12'),
    },
}

_CERT_PASSWORD='Haniprt1221!'

_headers = Headers(
    custom_fields={'Content-Type': 'application/json; charset=utf-8'}
)

def get_aps(msg, sound, badge=1):
    return APS(alert=msg, badge=badge, sound=sound)


def get_payload(aps: APS, custom_fields: dict):
    return Payload(aps=aps, custom_fields=custom_fields)


def send(did, app_name, push_mode, msg, sound, custom_fields):
    aps = get_aps(msg, sound)

    payload = get_payload(aps, custom_fields)

    client = Client(
        push_mode=push_mode,
        secure=True,
        cert_location=_CERT_PATH[app_name][push_mode],
        cert_password=_CERT_PASSWORD,
    )

    result = client.send(did, _headers, payload)
    print('### APS RESULT ###')
    print(result)
    print('##################')
