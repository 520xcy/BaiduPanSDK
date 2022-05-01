# BaiduPanSDK
因为NAS环境资源有限，用不了linux的百度网盘桌面端。最近发现百度网盘有开放平台接入了，干脆自己捣鼓了一个能在NAS上面跑的界面。

支持下载和删除网盘文件，下载支持断点续传。下载完后默认启用MD5验证。

## 申请密钥
https://pan.baidu.com/union/home
去官网申请

## 安装&使用
```
git clone https://github.com/520xcy/BaiduPanSDK.git
```
或直接下载解压
```
cd BaiduPanSDK
pip3 install -r requirments.txt
python3 web.py
```
首次运行后会自动在根目录生成```.env```文件，编辑它
```
{
"username": "admin", 
"password": "admin888",  #这是登录管理页面的用户名和密码，不是百度网盘的用户名密码
"ak": "", #开放平台申请到的AppKey
"at": "", #空
"sk": "", #SecretKey
"aid": "" #Appid
}
```
重新执行```python3 web.py```，看到服务已启动的提示后浏览器访问```http://IP:8182```

## 注意事项
默认下载存放在根目录下的Download文件夹内

linux要后台运行可以使用Screen等程序

