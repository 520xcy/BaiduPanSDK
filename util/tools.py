# -*- coding: utf-8 -*-
import os
import time

def mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def timeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

'''文件处理'''

def checkFileExist(fileURI):
    if os.path.isfile(fileURI):
        return True
    return False

def deleteFileFolder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            deleteFileFolder(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass

def writeFile(fileURI, str):
    with open(fileURI, 'w', encoding='UTF-8') as w:
        w.write(str)
    
def readFile(fileURI):
    with open(fileURI, 'r', encoding='UTF-8') as r:
        txt = r.read()
        return txt
