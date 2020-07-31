from enum import Enum


def format_object(api_error_type, result):
    code = api_error_type.value
    return {
        'errcode': code,
        'message': get_error_message(code),
        'data': result
    }


class Response:
    err_code = 0
    message = 'ok'
    result = any

    def format(self):
        return {
            'errcode': self.err_code,
             'msg': self.message,
            'data': self.result
        }


# 继承枚举类
class ApiErrorType(Enum):
    SUCCESS = 0
    UNRECOGNIZED = -1
    PARAMS = 1001
    UNKNOWN_PICTURE_FACE = 2001
    TARGET_PICTURE_EMPTY = 2002
    DECODE_BASE64_FAILED = 3001
    SERVER_ERROR = 500
    FAIL = 2003


def get_error_message(code):
    if ApiErrorType.SUCCESS.value == code:
        return '匹配成功'
    elif ApiErrorType.FAIL.value == code:
        return '匹配失敗'
    elif ApiErrorType.UNRECOGNIZED.value == code:
        return '圖片編碼不正確'
    elif ApiErrorType.UNKNOWN_PICTURE_FACE.value == code:
        return '图片不含有人脸，请核对'
    elif ApiErrorType.TARGET_PICTURE_EMPTY.value == code:
        return '人臉庫沒有此工號'
    elif ApiErrorType.PARAMS.value == code:
        return '传入参数爲空'
    elif ApiErrorType.SERVER_ERROR.value == code:
        return '服务器错误'
    elif ApiErrorType.DECODE_BASE64_FAILED.value == code:
        return '解析base64失败'
    else:
        return '识别失败'
