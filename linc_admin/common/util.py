from Crypto.Cipher import AES
from django.http import JsonResponse

from common.error_message import get_error_message


def res_json(error_code=0, data=None):
    result = {
        'error_code': error_code,
        'error_message': get_error_message(error_code),
    }

    if type(data) is dict:
        result['data'] = data

    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


def mysql_aes_float(val, key):
    try:
        return float(mysql_aes_decrypt(val, key))
    except:
        return 0.0


def mysql_aes_str(val, key, encoding='utf-8'):
    try:
        b = mysql_aes_decrypt(val, key)
        if b is None:
            return ''
        else:
            return b.decode(encoding)
    except:
        return ''


def mysql_aes_decrypt(val, key):

    def mysql_aes_key(key):
        final_key = bytearray(16)
        for i, c in enumerate(key):
            final_key[i % 16] ^= ord(key[i])
        return bytes(final_key)

    k = mysql_aes_key(key)

    cipher = AES.new(k, AES.MODE_ECB)

    padding_index = k.index(b'\x00')
    if padding_index > 0:
        dec = cipher.decrypt(val)
        return dec[0:dec.find(dec[-1])]
    else:
        return cipher.decrypt(val).decode()
