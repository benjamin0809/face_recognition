# -*- coding:utf-8 -*-

import datetime
import logging
import os
# from wsgiref import handlers
#
#
# def write_log(message):
#     logger = logging.getLogger()
#     rf_handler = handlers.TimedRotatingFileHandler(filename=os.path.abspath('.') + "/log/" + datetime.datetime.now().strftime('%Y-%m-%d') +".log", when='D', interval=1, backupCount=10)
#     logger.addHandler(rf_handler)
#     logger.setLevel(logging.INFO)
#     logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ':' + message)
#     logger.removeHandler(rf_handler)


def write_log(message):

    logger = logging.getLogger()
    handler = logging.FileHandler(get_file_path())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ':' + message)
    logger.removeHandler(handler)


def get_file_path():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    file_path = os.path.abspath('.') + "/log/%s.log" % today
    if os.path.isfile(file_path):
        print(123)
    return file_path

