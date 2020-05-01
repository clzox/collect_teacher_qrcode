"""
@Auth : chenyw
@Time : 2020-05-01-21:29
@File : checkQodeImage.py
"""
# encoding:utf-8


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

with open('config.json', encoding='utf-8') as f:
    info = json.load(f)
client = AipOcr(info['AppID'], info['API_Key'], info['Secret_Key'])


# 读取图片函数
def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


image = get_file_content('sample.png')

# 上传百度平台
img_info = client.basicGeneral(image)

# print(img_info['words_result_num'])
num = img_info['words_result_num']

for i in range(num):
    if img_info['words_result'][i]['words'].startswith('更新于'):
        upatde_time = img_info['words_result'][i]['words'].replace('更新于:', '')[:10]
        upatde_time = upatde_time.replace('-', '')
        print(upatde_time)
