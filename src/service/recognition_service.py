# -*- coding:utf-8 -*-

from config import Config
from src.common.app_uitility import read_file_from_base64
from src.common.error_code import ParameterException
from src.common.logger import write_log
from src.db.db_service import RedisService
from src.models.response import ApiErrorType
import face_recognition
import numpy as np


def get_encodings(base64):
    encoding_array = get_picture_encodings_base64(base64)
    return encodings_to_hex_str(encoding_array)


# 已知照片編碼
def get_source_picture_bytes(staff_no):
    byte = RedisService.redis_get(staff_no)
    if not byte:
        raise ParameterException(ApiErrorType.TARGET_PICTURE_EMPTY)
    byte = np.frombuffer(byte, dtype=float)
    return byte


# 照片對比
def identify_picture(base64_img, staff_no):
    picture_encodings = get_source_picture_bytes(staff_no)
    if len(picture_encodings) == 0:
        raise ParameterException(ApiErrorType.TARGET_PICTURE_EMPTY)

    target_picture_encodings = get_picture_encodings_base64(base64_img)
    if len(target_picture_encodings) == 0:
        raise ParameterException(ApiErrorType.UNKNOWN_PICTURE_FACE)
    results = face_recognition.compare_faces([picture_encodings], target_picture_encodings,
                                             tolerance=Config.tolerance)
    # # 輸出對比結果
    if True in results:
        return ApiErrorType.SUCCESS
    else:
        raise ParameterException(ApiErrorType.FAIL)


# 未知照片編碼
def get_picture_encodings_base64(base64):
    unknown_file = read_file_from_base64(base64)
    unknown_image = face_recognition.load_image_file(unknown_file)
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    if unknown_encodings == []:
        return []
    return unknown_encodings[0]


# 已知照片編碼
def get_picture_encodings(act_path_or_file):
    unknown_image = face_recognition.load_image_file(act_path_or_file)
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    return unknown_encodings[0]


# encodings 转换成十六进制字符串
def encodings_to_hex_str(encodings):
    encodings_bytes = encodings.tobytes()
    known_encoding_str = bytes.hex(encodings_bytes)
    return known_encoding_str


# 十六进制字符串 转换encodings
def encodings_hex_to_array(encodings_hex):
    db_encodings_bytes = bytes.fromhex(encodings_hex)
    db_unknown_encodings = np.frombuffer(db_encodings_bytes, dtype=float)
    return db_unknown_encodings



