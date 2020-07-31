from .error import APIException
from ..models.response import ApiErrorType, get_error_message


class ServerError(APIException):
    code = 500
    msg = "server is invalid"
    error_code = 999
    data = ''


class ParameterException(APIException):

    code = 200
    msg = 'invalid parameter'
    error_code = 0
    data = ''

    def __init__(self, error_code, msg=None, code=None, data=None):
        if isinstance(error_code, ApiErrorType):
            self.error_code = error_code.value
            if msg is not None:
                self.msg = msg
            else:
                self.msg = get_error_message(error_code.value)
        else:
            self.error_code = 0
        self.code = 200
        self.data = ''
        super(ParameterException, self).__init__(self.msg, code, self.error_code, data)


class AuthFailed(APIException):
    code = 401
    msg = '没授权'
    error_code = 4001
    data = ''


