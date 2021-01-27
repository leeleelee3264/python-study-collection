from common.error_code import *

_default_error_message = {
    # OK
    OK: '성공',

    # client
    ERROR_NO_PARAM: 'WARN! 필수 입력값을 입력하지 않았습니다.',
    ERROR_INVALID_PARAM: 'WARN! 입력한 값이 유효하지 않습니다.',
    ERROR_INVALID_PARAM_TYPE: 'WARN! 입력한 값의 타입이 유효하지 않습니다.',
    ERROR_NO_SESSION_KEY: 'WARN! 유저 확인을 위한 session key가 없습니다.',
    ERROR_INVALID_URL: 'WARN! 입력하신 url을 다시 확인해주세요.',
    ERROR_NOT_SUPPORTED_METHOD : 'WARN! 지원하지 않은 메소드 형태입니다.',

    # db
    ERROR_DB_ANSWER: 'ERROR! DB 에러가 발생했습니다.',

    # server
    ERROR_SERVER_INTERNAL: 'ERROR! 서버에 에러가 발생했습니다.'
}


def get_error_message(error_code):
    global _default_error_message

    return _default_error_message.get(error_code, 'unregistered error')
