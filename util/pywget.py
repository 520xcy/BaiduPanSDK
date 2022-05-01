# -*- coding: utf-8 -*-

import requests
import sys
import os
import re
import time
import hashlib
import requests
import threading


class wget(threading.Thread):
    tlist = {}  # 用来存储队列的线程
    # int(sys.argv[2])最大的并发数量，此处我设置为100，测试下系统最大支持1000多个
    maxthreads: int = os.cpu_count() or 1
    evnt = threading.Event()  # 用事件来让超过最大线程设置的并发程序等待
    lck = threading.Lock()  # 线程锁

    def __init__(self, url: str, filename: str, headers: dict = {}, total: int = 0, md5: str = '', fsids:str='',block: int = 1024):
        threading.Thread.__init__(self)
        self.config = {
            'block': block,
        }
        self.size = 0
        self.filename = ''
        self._size = 0
        self._speed = 0
        self.url = url
        self.local_filename = filename
        self._local_filename = self.local_filename
        self.headers = headers
        self.total = total
        self.md5 = md5
        self.connect = ''
        self.fsids = fsids
        self.__running = True

    def remove_nonchars(self, name):
        (name, _) = re.subn(r'[\\\/\:\*\?\"\<\>\|]', '', name)
        return name

    def run(self):

        try:
            block = self.config['block']
            _dirname = os.path.dirname(self.local_filename)
            try:
                os.makedirs(_dirname)
            except FileExistsError:
                pass
  
            self.filename = os.path.basename(self.local_filename)
            self.local_filename = os.path.join(_dirname, self.remove_nonchars(self.filename))

            if os.path.isfile(self.local_filename):
                _filename, _ext = os.path.splitext(self.filename)
                self.filename = _filename+'_'+str(int(time.time()))+_ext
                self.local_filename = os.path.join(os.path.dirname(
                    self.local_filename), self.remove_nonchars(self.filename))

            self.local_filename += '.pydownloading'
            if os.path.isfile(self.local_filename):
                self.size = os.path.getsize(self.local_filename)
                if self.size > self.total:
                    raise RuntimeError(f"{self.filename}File is wrong.")
                else:
                    self.headers['Range'] = "bytes=%d-" % (self.size, )
                    self._size = self.size + 1

            r = requests.get(self.url, stream=True,
                             verify=False, headers=self.headers)
            if self.total > 0:
                print("[+] Size: %dKB" % (self.total / 1024))
            else:
                print("[+] Size: None")
            start_t = time.time()

            d = {
                'file':self.filename,
                'localfile': self._local_filename,
                'size':self.total,
                'status':'Running',
                'fsids':self.fsids,
                'date':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                'connect':self.connect
            }
            self.sendStatus(**d)

            with open(self.local_filename, 'ab+') as f:
                f.seek(self.size)
                f.truncate()

                for chunk in r.iter_content(chunk_size=block):
                    if not self.__running:
                        raise RuntimeError('threading is stoped')
                    if chunk:
                        f.write(chunk)
                        self._size += len(chunk)
                        f.flush()
                    self._speed = int(
                        (self._size - self.size) / (time.time() - start_t))
                    sys.stdout.write(
                        '\b' * 64 + 'Now: %d, Total: %s, Speed: %dk/s' % (self._size, self.total, self._speed))
                    sys.stdout.flush()
                spend = int(time.time() - start_t)
                speed = int((self._size - self.size) / spend) if spend!=0 else 0
                sys.stdout.write(
                    '\nDownload Finished!\nTotal Time: %ss, Download Speed: %sk/s\n' % (spend, speed))
                sys.stdout.flush()
                self.connect = 'Finished!'
            if self.md5:
                with open(self.local_filename, 'rb') as fp:
                    data = fp.read()
                file_md5 = hashlib.md5(data).hexdigest()
                if self.md5 != file_md5:
                    self.connect = 'Finished and MD5 check wrong!'
                    sys.stdout.write('md5 check wrong!')
                else:
                    self.connect = 'Finished and MD5 check pass!'
                    sys.stdout.write('md5 check pass!')
                sys.stdout.flush()

        except Exception as e:
            print(str(e))

        else:
            os.rename(self.local_filename, self._local_filename)
            d = {
                'file':self.filename,
                'localfile': self._local_filename,
                'size':self.total,
                'status':'Done',
                'fsids':self.fsids,
                'date':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                'connect':self.connect
            }
            self.sendStatus(**d)

        finally:
            # 以下用来将完成的线程移除线程队列
            self.lck.acquire()
            del self.tlist[self.fsids]
            # 如果移除此完成的队列线程数刚好达到99，则说明有线程在等待执行，那么我们释放event，让等待事件执行
            if len(self.tlist) == self.maxthreads-1:
                self.evnt.set()
                self.evnt.clear()
            self.lck.release()

    def sendStatus(self, **params):
        response = requests.post("http://127.0.0.1:8182/api/update", data=params)
        if response.status_code != 200:
            print('状态发送失败')
        
    def stop(self):
        self.__running = False

    def newthread(url, output, headers, size, md5, fsids):
        wget.lck.acquire()  # 上锁
        sc = wget(url, output, headers, size, md5, fsids)
        wget.tlist[fsids] = sc
        wget.lck.release()  # 解锁
        sc.start()
    # 将新线程方法定义为静态变量，供调用
    newthread = staticmethod(newthread)
