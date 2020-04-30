"""
@Auth : chenyw
@Time : 2020-04-29-14:51
@File : processQodet.py
"""
import os
import pandas as pd
import searchfile

path = r'C:\Users\cheny\Desktop\教师随申码收集'
# 实例化搜索文件类，确定搜索的文件类型
sf = searchfile.Searchfile(path, target=['.xlsx'])
# 开始搜索文件
sf.search_file()
# 把搜索结果返回并赋值给指定列表423
file_list = sf.get_file(mode=2)
print(file_list)
# excel 转换成dataframe
teacher_list = pd.read_excel(r'C:\Users\cheny\Desktop\teacher_name.xlsx', index_col='教师姓名')
# 给dataframe添加一行名为xin 的空列
# teacher_list['xin'] = None
print(teacher_list)
for file in file_list:
    # 确定列名
    column_name = os.path.splitext(file)[0].split('\\')[-1]
    # print(column_name)
    # excel转换成dataframe
    exist_teacher = pd.read_excel(file, index_col='教师姓名')
    # exist_teacher.set_index('教师姓名')
    print(exist_teacher)
    # 关闭解释器的异常检测
    # noinspection PyBroadException
    try:
        # 根据文件名时间添加空列
        teacher_list[column_name + '随身码'] = ''
        teacher_list[column_name + '随申码图片'] = ''
        # print(filepd)
        for extea in exist_teacher.index:
            # print(exist_teacher.loc[str(extea), '随申码图片上传'])
            # 对照教师姓名添加相应信息
            teacher_list.loc[extea, column_name + '随身码'] = exist_teacher.loc[extea, '健康码']
            teacher_list.loc[extea, column_name + '随申码图片'] = exist_teacher.loc[extea, '随申码图片上传']
    except Exception as e:
        pass

teacher_list.to_excel('complete.xlsx')
