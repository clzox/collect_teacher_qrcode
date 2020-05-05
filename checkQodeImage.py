"""
@Auth : chenyw
@Time : 2020-05-01-21:29
@File : checkQodeImage.py
"""
import os

'''
返回结果示例：
{
"log_id": 2471272194,
"words_result_num": 2,
"words_result":
    [
        {"words": " TSINGTAO"},
        {"words": "青島睥酒"}
    ]
}
'''

import json
from aip import AipOcr
import searchfile
import pandas as pd

# 打开config.json，里面存放的是百度的数字ID，key以及密钥
with open('config.json', encoding='utf-8') as f:
    info = json.load(f)
# 建立客户端
client = AipOcr(info['AppID'], info['API_Key'], info['Secret_Key'])


# 读取图片二进制函数
def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


# 找到随申码所在的文件夹
path = r'C:\Users\cheny\Desktop\教师随申码收集'


# 这下面被注释掉的是整个使用百度ocr基本流程，只是放在这用来做代码样例用的
# image = get_file_content('sample.png')

# 上传百度平台
# img_info = client.basicGeneral(image)

# print(img_info['words_result_num'])
# num = img_info['words_result_num']

# for i in range(num):
#     if img_info['words_result'][i]['words'].startswith('更新于'):
#         upatde_time = img_info['words_result'][i]['words'].replace('更新于:', '')[:10]
#         upatde_time = upatde_time.replace('-', '')
#         print(upatde_time)

# 建立处理图片的基本函数，传入的是存有图片绝对路径的列表
def getimagelist(image_list):
    # 打开最后要保存的数据表格文件
    # 表格文件的表头应该是 图片名字、教师姓名、提交时间、图片时间、是否符合，顺序也不应该错，否则会与下方代码冲突
    complete_df = pd.read_excel('图片统计.xlsx')
    # 下方的英文作用是关闭解释器的exception异常检测，不写也可以
    # noinspection PyBroadException
    try:
        # 遍历图片列表，对于每一个图片进行处理
        for image in image_list:
            # 图片的名称从文件路径中读取
            image_name = os.path.splitext(image)[0].split('\\')[-1]
            # 提交问卷的时间从文件中的名字获取
            current_time = os.path.splitext(image)[0].split('\\')[-3]
            # 图片本身的更新时间，默认是不详
            update_time = '不详'
            # 图片上的教师姓名，默认是不详
            teacher_name = '不详'
            # 是否符合，默认是不详
            isok = '不详'
            # 把图片转化为二进制文件
            image_read = get_file_content(image)
            # 上传百度平台进行OCR，返回的数据类型见百度SDK文件
            img_info = client.basicGeneral(image_read)
            # 存放返回的字符串数量
            num = img_info['words_result_num']
            # 如果返回的字符串数量不等于零，则开始寻找有用信息
            if num != 0:
                for i in range(num):
                    # 寻找返回的数据的规律，发现可以定位字符串'更新于'用来找到时间
                    # 所以如果存在这个字符串，则说明找到了图片的更新时间
                    # 那么前面一条字符串必定是教师姓名，详情可见上海随申码的图片样式
                    # 每个地方的健康码不同，应该具体情况具体讨论，灵活变通
                    if img_info['words_result'][i]['words'].startswith('更新于'):
                        # 处理字符串，但会有误差，具体取决于ocr出来的字符串文本
                        # 把“更新于”去掉
                        # 这里应该用正则表达式更好一点，下次修改
                        update_time = img_info['words_result'][i]['words'].replace('更新于:', '')[:10]
                        update_time = update_time.replace('-', '')[:9]
                        # 对比提交时间与更新时间，验证是否符合
                        if update_time == current_time:
                            isok = '符合'
                        else:
                            isok = '不符合'
                        # 找到教师姓名
                        teacher_name = img_info['words_result'][i - 1]['words']
            # 把读取的数据打包成字典类型并加入df中，igonre_index意思是忽略加入时的index,遵照原始index顺序
            complete_df = complete_df.append([{'图片名字': image_name,
                                               '教师姓名': teacher_name,
                                               '提交时间': current_time,
                                               '图片时间': update_time,
                                               '是否符合': isok}], ignore_index=True)
    # 捕获异常并打印异常
    # 在pycharm中，这里可能会显示绿色波浪线，是因为解释器认为你捕获的异常太过宽泛，不恰当，提醒你
    # 如果要关闭可以在try之前写上那句英文
    except Exception as e:
        print(e)
    # 存入表格文件
    complete_df.to_excel('图片统计.xlsx', index=False)
    # 返回值，这里可以不需要返回值
    return complete_df


# 二次检查，这个函数还没有写好
def checksecond():
    image_df = pd.read_excel('图片统计.xlsx')
    for image in image_df.index:
        # print(image)
        print(image_df.loc[image, '是否符合'])
        if image_df.loc[image, '是否符合'] == '不符合':
            if str(image_df.loc[image, '提交时间']) in str(image_df.loc[image, '图片时间']):
                image_df.loc[image, '是否符合'] = '符合'
    image_df.to_excel('图片统计.xlsx')


# 首先保存初始工作路径
orignpath = os.getcwd()
# 进入存放文件的路径
os.chdir(path)
# 读取文件夹列表（这里要保证所有文件类型都是文件夹，有必要应该验证下）
filelist = os.listdir()
# 回到程序所在路径
os.chdir(orignpath)
# 打开记录log
f = open('image_read_log.txt', 'r+', encoding='utf-8')
# 转换成列表形式
tem_list = f.read().split('\n')
# 把最后一个空字符串pop出去
tem_list.pop()
# 对每个文件进行遍历，
for fl in filelist:
    # 如果这个文件夹不在读取的log文件夹列表里，就说明没有做过OCR
    if fl not in tem_list:
        # 首先把这个文件夹保存进log中，表示里面的图片已经OCR过了
        f.write(fl + '\n')
        # 把这个文件夹放入完整的路径之中，sep是斜杠
        realpath = path + os.sep + fl
        # 建立文件搜索类
        sf_image = searchfile.Searchfile(realpath, ['.jpeg'])
        # 进行文件搜索
        sf_image.search_file()
        # 在这里我们需要完整的文件绝对路径，所以选择mode=2
        image_l = sf_image.get_file(mode=2)
        # 把从文件夹中找到的图片放进函数中进行处理，返回值可以不需要的，我们不在这里存表格文件了
        complete = getimagelist(image_l)
        # complete.to_excel('图片统计.xlsx', index=False)

checksecond()
