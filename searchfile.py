"""
@Auth : chenyw
@Time : 2020-04-29-14:42
@File : searchfile.py
"""

import os


# 建立异常类
class Myexception(Exception):
    # 初始化信息提示
    def __init__(self):
        self.message_o = 'mode should be 1 or 2 or 3 and 1(default) : return <list:file_name_list>' \
                         ' or 2 : return <list:file_name_abs_path_list>' \
                         ' or 3 : return <dict :file_name_rel_path_list> '

    # 返回信息提示
    def __str__(self):
        return repr(self.message_o)


class Searchfile:
    def __init__(self, path, target):
        self.orign = os.getcwd()
        self.path = path
        self.target = target
        self.mode = 1
        self.file_name_list = []
        self.file_name_abs_path_list = []
        self.file_name_rel_path_list = {}

    def search_file(self,):
        os.chdir(self.path)
        # print('current file directory:{}'.format(os.getcwd()))
        for eachfile in os.listdir():
            if os.path.isfile(eachfile):
                # 获取文件的后缀名
                # splitext 函数返回的是一个元组，存放着文件名以及文件名后缀
                ext = os.path.splitext(eachfile)[1]
                if ext in self.target:
                    # 将文件名称加入文佳名称的列表中
                    self.file_name_list.append(eachfile)
                    # 将文件的绝对路径放进列表中
                    self.file_name_abs_path_list.append(os.getcwd() + os.sep + eachfile)
                    # 以文件名以及文件名所在的当前文件夹存储为键值对放在一个列表中
                    # os.path.abspath('.') 返回当前目录的绝对路径
                    # os.path.abspath('..') 返回上级目录的绝对路径
                    self.file_name_rel_path_list[eachfile] = os.getcwd().replace(os.path.abspath('..'), '', 1)[1:]
            if os.path.isdir(eachfile):
                self.path = eachfile
                # 递归调用
                self.search_file()
                # 防止无限递归
                os.chdir(os.pardir)

    def get_file(self, mode=1):
        if mode == 1:
            os.chdir(self.orign)
            return self.file_name_list

        elif mode == 2:
            os.chdir(self.orign)
            return self.file_name_abs_path_list
        elif mode == 3:
            os.chdir(self.orign)
            return self.file_name_rel_path_list
        else:
            os.chdir(self.orign)
            # 其他字符则引起错误并抛出错误
            raise Myexception()


if __name__ == "__main__":
    sf = Searchfile(os.getcwd(), ['.xlsx'])
    sf.search_file()
    try:
        print(sf.get_file(1))
    except Myexception as e:
        print(e.message_o)
