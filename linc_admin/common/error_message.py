from common.error_code import *

_error_message = {
    0: 'success',

    # PUSH MESSAGE
    PUSH_NO_MESSAGE: '메시지를 입력하십시오.',
    PUSH_NO_TARGET: '발송할 대상을 입력하십시오.',
    PUSH_INVALID_TARGET: '발송할 대상을 확인하시기 바랍니다.',

    # 유효기간 연장
    EXTEND_EXPIRE_NO_DAYS: '연장할 일수를 입력하십시오.',
    EXTEND_EXPIRE_NO_TARGET: '연장할 대상을 입력하십시오.',
    EXTEND_EXPIRE_INVALID_TARGET: '연장할 대상을 확인하시기 바랍니다.',

    # FW MODE 변경
    CHANGE_FW_MODE_NO_MODE: '펌웨어 모드(0-5)를 입력하십시오.',
    CHANGE_NO_TARGET: '변경할 대상을 입력하십시오.',
    CHANGE_INVALID_TARGET: '변경할 대상을 확인하시기 바랍니다.',

    # 로라 주기 변경
    CHANGE_LORA_PERIOD_NO_PERIOD: '로라 주기를 입력하십시오',

    # 배송
    DELIVER_NO_TARGET: '배송할 대상을 입력하십시오.',
    DELIVER_WRONG_EXPIRE_DAYS: '유효기간이 잘못되었습니다.',
    DELIVER_WRONG_START_DATE: '강제시작 일자가 잘못되었습니다.',
    DELIVER_MORE_START_DATE: '강제시작 일자를 오늘 이후로 입력해 주시기 바랍니다.',
    DELIVER_ALREADY_USE: '이미 사용중이거나 배송중인 디바이스가 있습니다.',
    DELIVER_NOT_EXPIRE: '만료일자가 남아있는 디바이스가 있습니다.',

    # 새 디바이스 등록
    NEW_DEVICE_INVALID_TP_ID: '기관 ID가 올바르지 않습니다.',
    NEW_DEVICE_WRONG_COUNTRY_CODE: '국가코드가 올바르지 않습니다.',
    NEW_DEVICE_FAIL: '디바이스 등록을 실패했습니다.',

    QLIQ_NO_PHONE_NUM: '폰번호가 존재하지 않습니다.',
    QLIQ_NO_DID: 'DID가 존재하지 않습니다.',

    PARAM_ERROR: '파라미터 오류',
    DB_ERROR: '데이테베이스 오류',
    PUSH_ERROR: 'PUSH 발송 오류',

    LOGIN_FAIL: '로그인을 실패했습니다.',
    LOGIN_REQUIRED: '로그인이 필요합니다.',
}


def get_error_message(error_code):
    global _error_message

    return _error_message.get(error_code, 'unknown error')
