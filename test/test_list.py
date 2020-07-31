import base64
import json

import face_recognition
import numpy as np
from flask import jsonify
import ast
from src.common.des import des_encrypt, des_decrypt
# from src.db.db_service import MSSQL


def test_encoding():
    act_path = 'H:\\app\\python\\face-recognition-service\\picture\\mine\\F2846595-extra2.JPG'
    unknown_image = face_recognition.load_image_file(act_path)
    # 未知編碼
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    # encodings ndarray convert to bytes
    encodings_bytes = unknown_encodings[0].tobytes()
    # bytes convert to hex string and save in db
    encodings_hex = bytes.hex(encodings_bytes)
    # query data; then convert to db_unknown_encodings
    db_encodings_bytes = bytes.fromhex(encodings_hex)
    db_unknown_encodings = np.frombuffer(db_encodings_bytes, dtype=float)

    # compare
    print(db_unknown_encodings)


def test_db():
    str1 = str()
    base64byte = des_encrypt(str1)
    base64str = str(base64byte, encoding='utf-8')

    ee = des_decrypt(base64str)
    ee = str(ee, encoding='utf-8')
    user_dict = ast.literal_eval(ee)
    print(user_dict)
test_db()
# # 數據查詢
# def select_photo_table(staff_no):
#     mssql = MSSQL()
#     try:
#         sql = "select base64str,encodingstr from [BasEmployeePhoto] where staffno=%s and id = %d"
#         args = (staff_no, 2)
#         photo_tb = mssql.ExecQuery(sql, args)
#         return photo_tb
#     except Exception as e:
#         return e
# select_photo_table('F2846595')