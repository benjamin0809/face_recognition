import face_recognition
import numpy as np
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

from config import Config
from src.common.app_uitility import read_file_from_base64
from src.common.error import APIException
from src.common.error_code import ParameterException, AuthFailed, ServerError
from src.common.logger import write_log
from src.db.db_service import RedisService
from src.models.response import format_object, ApiErrorType
from src.service import recognition_service

app = Flask(__name__)
recognition_prefix = 'api'


@app.before_request
def before_request():
    # token = request.headers.get('x-token')
    # if Config.api_key != token:
    #     raise AuthFailed()
    print("####")


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


# 首页
@app.route('/', methods=['GET'])
def index():
    return '''
    <!doctype html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>人脸服务</title>
    <a href="upload">人脸录入</a><br>
    <a href="search">人脸搜索</a>
    '''


# 人脸录入页
@app.route('/upload', methods=['GET'])
def upload_html():
    return '''
    <!doctype html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>人脸录入</title>
    <h1>人脸录入</h1>
    <form method="POST" action="api/upload" enctype="multipart/form-data">
      姓名：<input type="text" name="name"><br>
      <input type="file" name="file">
      <input type="submit" value="提交">
    </form>
    '''


# 人脸搜索页
@app.route('/search', methods=['GET'])
def search_html():
    return '''
    <!doctype html>
    <title>人脸搜索</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <h1>人脸搜索</h1>
    <form method="POST" action="api/search"  enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="提交">
    </form>
    '''


# 人脸录入
@app.route('/%s/upload' % recognition_prefix, methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'code': 500, 'msg': '没有文件'})
    file = request.files['file']
    if not file.filename:
        raise ParameterException(ApiErrorType.PARAMS, 'file.filename must be called')
    filename = file.filename.split('.', 1)[0]
    name = request.form['name']
    if len(name) > 0:
        filename = name
    image = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) != 1:
        return jsonify({'code': 500, 'msg': '人脸数量有误'})
    face_encodings = face_recognition.face_encodings(image, face_locations)
    # 连数据库

    bytes_ = face_encodings[0].tobytes()
    RedisService.redis_set(filename, bytes_)
    return jsonify(format_object(ApiErrorType.SUCCESS, '录入成功'))


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


# 人脸搜索
@app.route('/%s/search' % recognition_prefix, methods=['POST'])
def search():
    if 'file' not in request.files:
        return jsonify({'code': 500, 'msg': '没有文件'})
    file = request.files['file']
    image_ = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image_)
    if len(face_locations) != 1:
        return jsonify({'code': 500, 'msg': '人脸数量有误'})
    face_encodings = face_recognition.face_encodings(image_, face_locations)
    faces = RedisService.redis_get_all()
    # 组成矩阵，计算相似度（欧式距离）
    matches = face_recognition.compare_faces([np.frombuffer(x) for x in faces], face_encodings[0],
                                             tolerance=Config.tolerance)
    return jsonify({'code': 0, 'names': [str(name, 'utf-8') for name, match in zip(RedisService.redis_get_names(), matches) if match]})


# 人脸搜索
@app.route('/%s/find' % recognition_prefix, methods=['POST'])
def find():
    data = request.get_json()
    base64str = data.get("base64str")
    if not base64str or len(base64str) == 0:
        raise ParameterException(ApiErrorType.PARAMS, 'base64str must be called')
    file = read_file_from_base64(base64str)
    image = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) != 1:
        return jsonify({'code': 500, 'msg': '人脸数量有误'})
    face_encodings = face_recognition.face_encodings(image, face_locations)
    faces = RedisService.redis_get_all()
    # 组成矩阵，计算相似度（欧式距离）
    matches = face_recognition.compare_faces([np.frombuffer(x) for x in faces], face_encodings[0],
                                             tolerance=Config.tolerance)
    return jsonify({'code': 0, 'names': [str(name, 'utf-8') for name, match in zip(RedisService.redis_get_names(), matches) if match]})


# 清空redis key
@app.route('/%s/clear' % recognition_prefix, methods=['POST'])
def clear():
    data = request.get_json()
    staff_no = data.get("staff_no")
    if not staff_no or len(staff_no) == 0:
        raise ParameterException(ApiErrorType.PARAMS, 'staff_no must be called')

    RedisService.redis_clear_key(staff_no)
    return jsonify(format_object(ApiErrorType.SUCCESS, 'ok'))


#  keys
@app.route('/%s/keys' % recognition_prefix, methods=['GET'])
def keys():
    list1 = RedisService.redis_keys_all()
    results = list()
    for letter in list1:  # 第一个实例
        res = str(letter)
        results.append(res)
    return jsonify(format_object(ApiErrorType.SUCCESS, results))


def get_define_app():
    return app
