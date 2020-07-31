# -*- coding:utf-8 -*-

from config import Config
from src.common.app_uitility import read_file_from_base64
from src.common.error_code import ParameterException
from src.common.logger import write_log
from src.models.response import ApiErrorType
import face_recognition
import numpy as np


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



