##### collect_teacher_qrcode
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