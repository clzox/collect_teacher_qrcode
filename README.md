##### collect_teacher_qrcode
###### 20200505 update
1.完善了checksecond函数，该函数的功能为重新检查current_time和update_time，如果current_time和update_time有部分重合，便把不符合改为符合
###### 20200504 update
1.完善了存入表格文件时的逻辑，把存文件放在函数之内，确保每一次打开添加在末尾之后都能及时存放  
2.完善了校验图片是否已经OCR的逻辑，把文件夹作为验证，已经验证过的文件夹名称写入image_read_log.txt中，每次开始之前读取文件夹列表并遍历，如果已经在log中了，
就不用再从中读取图片列表了，也就减少了读取之后图片列表的长度。  
<pre>
    <code>
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
        f.write(fl+'\n')
        # 把这个文件夹放入完整的路径之中，sep是斜杠
        realpath = path+os.sep+fl
        # 建立文件搜索类
        sf_image = searchfile.Searchfile(realpath, ['.jpeg'])
        # 进行文件搜索
        sf_image.search_file()
        # 在这里我们需要完整的文件绝对路径，所以选择mode=2
        image_l = sf_image.get_file(mode=2)
        # 把从文件夹中找到的图片放进函数中进行处理，返回值可以不需要的，我们不在这里存表格文件了        
        complete = getimagelist(image_l)
        # complete.to_excel('图片统计.xlsx', index=False)
f.close()
    </code>
</pre>  
3.给大部分代码添加了注释
###### 20200501 update
1.添加了code_log.txt,processQodet.py读取之后用以记录已添加进excel的文件  

2.记录的excel文件与原始的teacher_name.xlsx重合，换言之，统一了最后保存的表格文件
<pre>
    <code>
teacher_list.to_excel('teacher_name.xlsx')
    </code>
</pre>

3.尝试利用baidu的ocr识别随申码上的更新时间，与实际老师提交的问卷时间做对比，找出不是当天的随申码
。但是百度ocr的次数有限，无法一直尝试debug，只能慢慢来。

