# -*- coding:utf-8 -*-

from config import Config
from src.common.app_uitility import read_file_from_base64
from src.common.error_code import ParameterException
from src.common.logger import write_log
from src.models.response import ApiErrorType
import face_recognition
from src.service.photo_service import select_photo_table, update_photo_table
import numpy as np


# 已知照片編碼
def get_source_picture_encodings(staff_no):
    try:
        photo_tb = select_photo_table(staff_no)
        if not photo_tb:
            return list()
        encoding_str = photo_tb[0]['encodingstr']
        if encoding_str is None:
            base64str = photo_tb[0]['base64str']
            base64_img_bytes = read_file_from_base64(base64str)

            known_encoding = get_picture_encodings(base64_img_bytes)
            update_photo_table(staff_no, encodings_to_hex_str(known_encoding))
        else:
            db_encodings_bytes = bytes.fromhex(encoding_str)
            known_encoding = np.frombuffer(db_encodings_bytes, dtype=float)
        return known_encoding
    except Exception as e:
        write_log('get_source_picture_encodings to error:{}'.format(str(e)))
        return e


def get_encodings(base64):
    encoding_array = get_picture_encodings_base64(base64)
    return encodings_to_hex_str(encoding_array)


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


# 照片對比
def identify_picture(base64_img, staff_no):
    picture_encodings = get_source_picture_encodings(staff_no)
    if len(picture_encodings) == 0:
        raise ParameterException(ApiErrorType.TARGET_PICTURE_EMPTY)

    target_picture_encodings = get_picture_encodings_base64(base64_img)
    if len(target_picture_encodings) == 0:
        raise ParameterException(ApiErrorType.UNKNOWN_PICTURE_FACE)
    results = face_recognition.compare_faces([picture_encodings], target_picture_encodings, tolerance=Config.tolerance)
    # # 輸出對比結果
    if True in results:
        return ApiErrorType.SUCCESS
    else:
        raise ParameterException(ApiErrorType.FAIL)



