# -*- coding: utf-8 -*-

from crypt import methods
import os
import socket
from waitress import serve
from flask import Flask, render_template, request, url_for, jsonify, abort, Blueprint, make_response
from datetime import timedelta
from util.log import get_logger
from util import tools
from util.baidupan import baidupan
# from watchdog.events import FileSystemEventHandler
# from watchdog.observers import Observer
from multiprocessing import Process, Pool, RLock, freeze_support
from util.shelvehelper import ShelveHelp
import json
from flask_bcrypt import Bcrypt
from flask_cors import CORS

BASE_PATH = os.getcwd()
TOKEN_PATH = os.path.join(BASE_PATH, '.token')

shelve = ShelveHelp(os.path.join(BASE_PATH, '.task'))

global DEVICE_CODE
DEVICE_CODE = ''
log = get_logger(__name__, 'ERROR')
ENV_PATH = os.path.join(BASE_PATH, '.env')
DOWNLOAD_PATH = os.path.join(BASE_PATH, 'download')

tools.mkdir(DOWNLOAD_PATH)

if tools.checkFileExist(ENV_PATH):
    ENV = json.loads(tools.readFile(ENV_PATH))
else:
    ENV = {'username': 'admin', 'password': 'admin888',
           'ak': '', 'sk': '', 'aid': ''}
    tools.writeFile(ENV_PATH, json.dumps(ENV))
    print('请先在.env文件内配置开放平台密钥')
    exit()

baidu = baidupan(
    ak=ENV['ak'],
    at='',
    sk=ENV['sk'],
    aid=ENV['aid'],
    dpath=DOWNLOAD_PATH
)
# download = Blueprint('download', __name__,
#                      static_folder=os.path.join(BASE_PATH, 'download'))

app = Flask(__name__, template_folder=os.path.join(BASE_PATH, 'template'),
            static_folder=os.path.join(BASE_PATH, 'template'), static_url_path='')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=0)
bcrypt = Bcrypt(app)
CORS(app)
# app.register_blueprint(download)


def setHash(pwd: str):
    return bcrypt.generate_password_hash(pwd.encode('utf-8'))


def checkHash(hash: str, pwd: str):
    return bcrypt.check_password_hash(hash, pwd.encode('utf-8'))


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/api/login', methods=['POST'])
def login():
    res = request.get_json()
    user = res['user'] if 'user' in res else ''
    password = res['password'] if 'password' in res else ''
    if user == str(ENV['username']) and password == str(ENV['password']):
        key = str(user)+str(password)
        hash = setHash(key)
        return jsonify({"code": 200, "message": "登录成功", "token": hash.decode()})
    else:
        return jsonify({"code": 0, "message": "登录失败"})


@app.route('/api/code', methods=['GET'])
def getCode():
    try:
        res = baidu.getCode()
        global DEVICE_CODE
        DEVICE_CODE = res['device_code']
        return jsonify({"code": 200, "data": {'verification_url': res['verification_url'], 'user_code': res['user_code'], 'qrcode_url': res['qrcode_url']}})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/at', methods=['GET'])
def getAccessToken():
    try:
        global DEVICE_CODE
        print(DEVICE_CODE)
        res = baidu.getAccessToken(DEVICE_CODE)
        baidu.setAt(res['access_token'])
        tools.writeFile(TOKEN_PATH, res['access_token'])
        return jsonify({"code": 200, "message": "ok"})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/userinfo', methods=['GET'])
def getUserinfo():
    try:
        res = baidu.getUserinfo()
        return jsonify({"code": 200, "data": res})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/size', methods=['GET'])
def getSize():
    try:
        res = baidu.getSize()
        return jsonify({"code": 200, "data": res})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/list', methods=['GET'])
def getList():
    try:
        dir = request.values.get('dir') if request.values.get('dir') else '/'
        order = request.values.get('order')
        start = int(request.values.get(
            'start')) if request.values.get('start') else 0
        limit = int(request.values.get(
            'limit')) if request.values.get('limit') else 20
        desc = request.values.get('desc')
        recursion = int(request.values.get('recursion')
                        ) if request.values.get('recursion') else 0
        res = baidu.getListall(dir=dir, start=start, limit=limit,
                               order=order, desc=desc, recursion=recursion)
        return jsonify({"code": 200, "data": res})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/meta', methods=['POST'])
def getFilemeta():
    try:
        fsids = request.get_json()['fsids']
        res = baidu.getFilemeta(fsids=fsids)
        return jsonify({"code": 200, "data": res})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/download', methods=['POST'])
def getFiles():
    try:
        fsids = request.get_json()['fsids']
        res = baidu.getFiles(fsids=fsids, needmd5=True)
        return jsonify({"code": 200, "data": res})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/run', methods=['GET'])
def getRun():
    try:
        res = baidu.getRun()
        return jsonify({"code": 200, "data": res})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/stop', methods=["POST"])
def getStop():
    try:
        fsids = request.get_json()['fsids']
        res = baidu.getStop(fsids)
        return jsonify({"code": 200, "data": res})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/update', methods=['POST'])
def updateTask():
    try:
        file = request.values.get('file')
        localfile = request.values.get('localfile')
        size = request.values.get('size')
        status = request.values.get('status')
        fsids = request.values.get('fsids')
        date = request.values.get('date')
        connect = request.values.get('connect')

        d = {
            localfile: {
                'localfile': localfile,
                'file': file,
                'size': size,
                'status': status,
                'fsids': fsids,
                'date': date,
                'connect': connect
            }
        }
        shelve.update(False, **d)
        return jsonify({"code": 200, "data": d})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/status', methods=['GET'])
def getStatus():
    try:
        res = shelve.read().values()
        return jsonify({"code": 200, "data": list(res)})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/deltask', methods=["POST"])
def delStatus():
    try:
        key = request.get_json()['key']
        return jsonify({"code": 200, "data": shelve.trash(key)})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.route('/api/delfiles', methods=["POST"])
def delFiles():
    try:
        files = request.get_json()['files']
        res = baidu.delFiles(list(files))
        return jsonify({"code": 200, "data": res})
    except Exception as e:
        log.error(str(e))
        return jsonify({"code": 0, "message": str(e)})


@app.before_request
def checkToken(*args, **kwargs):

    if request.path == '/api/login' or not request.path.startswith('/api') or request.method == 'OPTIONS':
        return
    if 'Baidusdk' in request.headers:
        reqtoken = request.headers.get('Baidusdk')
        hashtext = str(ENV['username'])+str(ENV['password'])
        if checkHash(reqtoken, hashtext):
            return
    return make_response(jsonify({"code": 0, "message": '请重新登录'}), 401)


def webrun():
    log.critical('web启动成功')
    serve(app, host='0.0.0.0', port=8182)
    log.critical('web停止')

# def watchdog():
#     event_handler = FileMonitorHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path=os.path.join(
#         BASE_PATH, 'contents'), recursive=True)  # recursive递归的
#     observer.start()
#     log.critical('文件夹监控启动')
#     observer.join()
#     log.critical('文件夹监控停止')


if __name__ == '__main__':
    if tools.checkFileExist(TOKEN_PATH):
        baidu.setAt(tools.readFile(TOKEN_PATH))

    freeze_support()
    # webbrowser.open("http://127.0.0.1:8181")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8182))
    if result == 0:
        log.error('socket端口被占用')
    else:
        try:
            webrun()
        except KeyboardInterrupt:
            pass
