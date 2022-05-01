# -*- coding: utf-8 -*-
import os
import time
import datetime

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

def get_day_time(n:float):
    the_date = datetime.datetime.now()
    pre_date = the_date + datetime.timedelta(days=n)
    pre_date = pre_date.strftime('%Y-%m-%d %H:%M:%S')#将日期转换为指定的显示格式
    pre_time = time.strptime(pre_date, "%Y-%m-%d %H:%M:%S") #将时间转化为数组形式
    pre_stamp = int(time.mktime(pre_time)) #将时间转化为时间戳形式
    return pre_stamp
