from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

from config import Config
from src.common.error import APIException
from src.common.error_code import ParameterException, AuthFailed, ServerError
from src.common.logger import write_log
from src.models.response import format_object, ApiErrorType
from src.service import recognition_service

app = Flask(__name__)
recognition_prefix = 'face'


@app.before_request
def before_request():
    token = request.headers.get('x-token')
    if Config.api_key != token:
        raise AuthFailed()


@app.errorhandler(Exception)
def framework_error(e):
    # 判断异常是不是APIException
    if isinstance(e, APIException):
        return e
    # 判断异常是不是HTTPException
    if isinstance(e, HTTPException):
        # log.error(e)
        code = e.code
        # 获取具体的响应错误信息
        msg = e.description
        error_code = 1007
        return APIException(code=code, msg=msg, error_code=error_code)
    # 异常肯定是Exception
    else:
        # 如果是调试模式,则返回e的具体异常信息。否则返回json格式的ServerException对象！
        # 针对于异常信息，我们最好用日志的方式记录下来。
        if app.config["DEBUG"]:
            # log.error(temp.format(info.f_code.co_filename, info.f_lineno, name, repr(e)))
            write_log('post_picture to error:{}'.format(str(e)))
            return e
        else:
            write_log('post_picture to error:{}'.format(str(e)))
            return ServerError()


@app.route('/%s/recognition' % recognition_prefix, methods=['POST'])
def recognition():
    data = request.get_json()

    base64str = data.get("base64str")
    staff_no = data.get("staff_no")

    if not staff_no or len(staff_no) == 0:
        raise ParameterException(ApiErrorType.PARAMS, 'staff_no must be called')

    if not base64str or len(base64str) == 0:
        raise ParameterException(ApiErrorType.PARAMS, 'base64str must be called')

    code = recognition_service.identify_picture(base64str, staff_no)
    return jsonify(format_object(code, 'ok'))


@app.route('/%s/encodings' % recognition_prefix, methods=['POST'])
def encodings():
    data = request.get_json()
    base64str = data.get("base64str")
    if not base64str or len(base64str) == 0:
        raise ParameterException(ApiErrorType.PARAMS, 'base64str must be called')
    res = recognition_service.get_encodings(base64str)
    return jsonify(format_object(ApiErrorType.SUCCESS, res))


def get_define_app():
    return app
