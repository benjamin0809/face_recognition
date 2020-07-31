# -*- coding:utf-8 -*-

# 數據庫連接
from src.common.logger import write_log
from src.db.db_service import MSSQL

mssql = MSSQL()


# 數據查詢
def select_photo_table(staff_no):
    try:
        sql = "select base64str,encodingstr from [BasEmployeePhoto] where staffno=%s"
        photo_tb = mssql.exec_query(sql, staff_no)
        return photo_tb
    except Exception as e:
        write_log('select_photo_table to error:{}'.format(str(e)))
        return e


# 數據更新
def update_photo_table(staff_no, encoding_str):
    try:
        sql = "update a set encodingstr=%s from [BasEmployeePhoto] a where staffno=%s"
        mssql.exec_non_query(sql, (encoding_str, staff_no))
    except Exception as e:
        write_log('update_photo_table to error:{}'.format(str(e)))
        return e





