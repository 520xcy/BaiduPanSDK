# -*- coding: utf-8 -*-
# 参考文档 https://pan.baidu.com/union/home
import requests
import json
import os
from util.pywget import wget
from util.tools import mkdir


class baidupan(object):

    def __init__(self, ak, sk, aid, at, dpath):
        self.ak = ak
        self.sk = sk
        self.aid = aid
        self.at = at
        self.dpath = dpath

    def setAt(self, at):
        self.at = at

    def getUrl(self, url: str, payload: dict = {}, headers: dict = {}):
        response = requests.request(
            method="GET", url=url, params=payload, headers=headers)
        if response.status_code == 200:
            res = json.loads(response.text.encode('utf8'))
            if 'error' in res:
                raise RuntimeError(res['error_description'])
            if 'errno' in res:
                if res['errno'] != 0:
                    raise RuntimeError('errno:'+str(res['errno'])+' info:'+','.join(res['info']))

            return res
        else:
            raise RuntimeError(response.text)

    def postUrl(self, url: str, data: dict = {}, headers: dict = {}):
        response = requests.request(
            method="POST", url=url, data=data, headers=headers)
        if response.status_code == 200:
            res = json.loads(response.text.encode('utf8'))
            if 'error' in res:
                raise RuntimeError(res['error_description'])
            if 'errno' in res:
                if res['errno'] != 0:
                    raise RuntimeError('errno:'+str(res['errno'])+' info:'+','.join(res['info']))
            return res
        else:
            raise RuntimeError(response.text)

    def getCode(self):
        url = "https://openapi.baidu.com/oauth/2.0/device/code"
        payload = {
            'response_type': 'device_code',
            'client_id': self.ak,
            'scope': 'basic,netdisk'
        }
        return self.getUrl(url, payload=payload)

    def getAccessToken(self, code: str):
        url = "https://openapi.baidu.com/oauth/2.0/token"
        payload = {
            'grant_type': 'device_token',
            'code': code,
            'client_id': self.ak,
            'client_secret': self.sk
        }
        return self.getUrl(url, payload=payload)

    def getUserinfo(self):
        url = "https://pan.baidu.com/rest/2.0/xpan/nas"
        payload = {
            'method': 'uinfo',
            'access_token': self.at
        }
        return self.getUrl(url, payload=payload)

    def getSize(self):
        url = "https://pan.baidu.com/api/quota"
        headers = {'User-Agent': 'pan.baidu.com'}
        payload = {
            'access_token': self.at,
            'checkfree': 1,
            'checkexpire': 1
        }
        return self.getUrl(url, headers=headers, payload=payload)

    def getList(self, **data):
        headers = {'User-Agent': 'pan.baidu.com'}
        payload = {
            'method': 'list',
            'web': 1,
            'folder': 0,
            'access_token': self.at,
            'order': data['order'] if 'order' in data else 'time',
            'dir': data['dir'] if 'dir' in data else '/',
            'start': data['start'] if 'start' in data else '0',
            'limit': data['limit'] if 'limit' in data else '20',
            'desc': data['desc'] if 'desc' in data else 'desc'
        }
        url = "https://pan.baidu.com/rest/2.0/xpan/file"
        return self.getUrl(url, headers=headers, payload=payload)

    def getFilemeta(self, fsids: list, **data):

        headers = {'User-Agent': 'pan.baidu.com'}
        payload = {
            'access_token': self.at,
            'method': 'filemetas',
            'fsids': json.dumps([int(fsid) for fsid in fsids ]),
            'dlink': data['dlink'] if 'dlink' in data else 0,
            'thumb': data['thumb'] if 'thumb' in data else 0,
            'extra': data['extra'] if 'extra' in data else 0,
            'needmedia': data['needmedia'] if 'needmedia' in data else 0
        }
        url = "https://pan.baidu.com/rest/2.0/xpan/multimedia"
        return self.getUrl(url, headers=headers, payload=payload)

    def getListall(self, **data):
        headers = {'User-Agent': 'pan.baidu.com'}
        payload = {
            'method': 'listall',
            'web': 1,
            'recursion': data['recursion'] if 'recursion' in data else 0,
            'access_token': self.at,
            'order': data['order'] if 'order' in data else 'time',
            'path': data['dir'] if 'dir' in data else '/',
            'start': data['start'] if 'start' in data else 0,
            'limit': data['limit'] if 'limit' in data else 20,
            'desc': data['desc'] if 'desc' in data else 'desc',
            'ctime': 0,
            'mtime': 0
        }
        url = "https://pan.baidu.com/rest/2.0/xpan/multimedia"
        return self.getUrl(url, headers=headers, payload=payload)

    def getFiles(self, fsids: list,  needmd5: bool = False):
        error = []
        _dlist = []
        _fsids = []
        res = self.getFilemeta(fsids, dlink=1)
        if res['list']:
            for i in res['list']:
                if i['isdir'] == 0:
                    _dlist.append(i)
                else:
                    _res = self.getListall(dir=i['path'], limit=9999)
                    for _i in _res['list']:
                        if _i['isdir'] == 0:
                            _fsids.append(_i['fs_id'])
            _res = self.getFilemeta(_fsids, dlink=1)
            if _res['list']:
                for _i in _res['list']:
                    _dlist.append(_i)

        headers = {
            'User-Agent': 'pan.baidu.com'
        }
        for i in _dlist:
            if not i['fs_id'] in wget.tlist:
                output = os.path.join(self.dpath, i['path'].lstrip('/'))

                url = i['dlink']+f"&access_token={self.at}"
                size = i['size']
                if needmd5:
                    md5 = i['md5']
                else:
                    md5 = ''

                # 如果目前线程队列超过了设定的上线则等待。
                wget.lck.acquire()
                if len(wget.tlist) >= wget.maxthreads:
                    wget.lck.release()
                    wget.evnt.wait()  # wget.evnt.set()遇到set事件则等待结束
                else:
                    wget.lck.release()
                wget.newthread(url, output, headers,
                               size, md5, i['fs_id'])
            else:
                error.append(output)
        return error

    def delFiles(self, files: list):
        headers = {'User-Agent': 'pan.baidu.com'}
        data = {
            'async': 2,
            'filelist': json.dumps([{'path': file} for file in files])
        }
        url = f"https://pan.baidu.com/rest/2.0/xpan/file?method=filemanager&access_token={self.at}&opera=delete"
        return self.postUrl(url, data, headers)

    def getRun(self):
        res = []
        for id in wget.tlist:
            res.append({
                'fs_id': id,
                'filename': wget.tlist[id].filename,
                'local_filename': wget.tlist[id].local_filename,
                'size': wget.tlist[id]._size,
                'total': wget.tlist[id].total,
                'speed': wget.tlist[id]._speed
            })
        return res

    def getStop(self, stopid: list):
        res = []
        for id in wget.tlist:
            if id in [int(fsid) for fsid in stopid]:
                res.append(id)
                wget.tlist[id].stop()
        return res
