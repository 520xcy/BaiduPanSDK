# -*- coding: utf-8 -*-
import shelve


def return_msg(code=200, msg="ok", data=None):
    """
    返回数据
    """
    return {
        "code": code,
        "msg": msg,
        "data": data,
    }


class ShelveHelp(object):
    """
    shelve简单的使用
    """

    def __init__(self, filename, flag="c"):
        self.filename = filename
        self.flag = flag

    def write(self, **kwargs):
        """
        写入数据
        执行代码之后会生成三个文件，分别是：{name}.bak     {name}.dat     {name}.dir
        """
        with shelve.open(filename=self.filename, flag=self.flag) as db:
            for k, v in kwargs.items():
                db[k] = v
        return 'ok'

    def get_data_keys(self):
        """
        获取数据key列表
        """
        with shelve.open(filename=self.filename, flag=self.flag) as db:
            keys = list(db.keys())
            return keys

    def read(self):
        """
        读取数据
        """
        with shelve.open(filename=self.filename, flag=self.flag) as db:
            keys = list(db.keys())
            result = {}
            for k in keys:
                result[k] = db[k]
            return result

    def get_one(self, key: str):
        alldb = self.read()
        if key in alldb.keys():
            return alldb[key]
        return None

    def trash(self, trash_key: list):
        """
        删除指定key数据
        """
        with shelve.open(filename=self.filename, flag=self.flag) as db:
            keys = list(db.keys())
            for _key in trash_key:
                if _key in keys:
                    del db[_key]
            return 'ok'

    def update(self, clear_all=False, **kwargs):
        """
        更新数据
        clear_all=True, 清除前面数据再写入，False，追加数据，相同key时会进行覆盖旧数据
        """
        with shelve.open(filename=self.filename, flag=self.flag) as db:
            if clear_all:
                keys = list(db.keys())
                for k in keys:
                    del db[k]
            if len(kwargs) > 0:
                for k, v in kwargs.items():
                    db[k] = v
            return 'ok'


def run():
    cls = ShelveHelp("test", flag="c")

    def simple_write():
        return cls.write(**{'h': 8888888, 'name': 99999, 'list': [1, 2, 3, 4, 5]})

    def simple_read():
        return cls.read()

    def simple_trash(key):
        return cls.trash(key)

    def simple_update():
        d = {
            "test": "test",
            "trash": "trash",
            "dfdfdfd": "dfdfdfd",
            "list": [1, 3, 4]
        }
        return cls.update(False, **d)

    # 写入
    # res = simple_write()

    # 读取
    res = simple_read()

    # 废弃
    # res = simple_trash("name")

    # 更新
    # res = simple_update()
    print(res)


def test_writeback():
    """
    测试回写功能（writeback=True）
    shelve访问己有key时，实际上取出的是数据源给出的一份拷贝，所以对于拷贝做出的增加和删除等操作都需要用writeback=True参数才能实现写入回文件中进行修改
    """
    with shelve.open(filename="hello", flag="c", writeback=True) as db:
        db['list'] = [1, 2, 3]

        # append
        # 当writeback=False, 对数据进行修改只是在内存中的修改，修改后的数据并没有被真正写入到文件中。
        db['list'].append(4)

        # remove
        db['list'].pop(1)

        print(db['list'])


if __name__ == '__main__':
    run()
