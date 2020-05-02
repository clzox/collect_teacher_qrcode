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

with open('config.json', encoding='utf-8') as f:
    info = json.load(f)
client = AipOcr(info['AppID'], info['API_Key'], info['Secret_Key'])


# 读取图片函数
def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


path = r'C:\Users\cheny\Desktop\教师随申码收集'
sf_image = searchfile.Searchfile(path, ['.jpeg'])
sf_image.search_file()
image_l = sf_image.get_file(mode=2)


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

def getimagelist(image_list):
    complete_df = pd.read_excel('图片统计.xlsx', columns=['图片名字', '教师姓名', '提交时间', '图片时间', '是否符合'])
    # 关闭解释器的异常检测
    # noinspection PyBroadException
    try:
        for image in image_list:
            image_name = os.path.splitext(image)[0].split('\\')[-1]
            current_time = os.path.splitext(image)[0].split('\\')[-3]
            update_time = '不详'
            teacher_name = '不详'
            isok = '不详'
            ff = open('image_read_log.txt', 'r+', encoding='utf-8')
            tem_list = ff.read().split('\n')
            tem_list.pop()
            if current_time not in tem_list:
                image_read = get_file_content(image)
                img_info = client.basicGeneral(image_read)
                num = img_info['words_result_num']
                if num != 0:
                    for i in range(num):
                        if img_info['words_result'][i]['words'].startswith('更新于'):
                            update_time = img_info['words_result'][i]['words'].replace('更新于:', '')[:10]
                            update_time = update_time.replace('-', '')[:9]
                            if update_time == current_time:
                                isok = '符合'
                            else:
                                isok = '不符合'
                            teacher_name = img_info['words_result'][i - 1]['words']
                complete_df = complete_df.append([{'图片名字': image_name,
                                                   '教师姓名': teacher_name,
                                                   '提交时间': current_time,
                                                   '图片时间': update_time,
                                                   '是否符合': isok}], ignore_index=True)
                f.write(current_time + '\n')
            f.close()
    except Exception as e:
        pass
    return complete_df


complete = getimagelist(image_l)
complete.to_excel('图片统计.xlsx', index=False)
