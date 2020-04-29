"""
@Auth : chenyw
@Time : 2020-04-29-14:51
@File : processQodet.py
"""
import os
import pandas as pd
import searchfile

# 实例化搜索文件类，确定搜索的文件类型
sf = searchfile.Searchfile(os.getcwd(), target=['.xlsx'])
# 开始搜索文件
sf.search_file()
# 把搜索结果返回并赋值给指定列表
file_list = sf.get_file(mode=2)
# print(file_list)
for file in file_list:
    filepd = pd.read_excel(file)
    print(filepd)
