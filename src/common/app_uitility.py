# -*- coding:utf-8 -*-
import re
from io import BytesIO
import base64
# 从base64字符串读取文件
from src.common.error_code import ParameterException
from src.models.response import ApiErrorType


def read_file_from_base64(base64img):
    base64_data = re.sub('^data:image/.+;base64,', '', base64img)
    try:
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
    except Exception as e:
        raise ParameterException(ApiErrorType.DECODE_BASE64_FAILED)
    return image_data



