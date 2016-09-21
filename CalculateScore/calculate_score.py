#-*- coding:utf-8 -*-

import re

with open('score.txt','r') as f:
    datas = f.readlines()

result = {}    # name:(score,times)
re_name = re.compile(r'[^\d ]+')    # 非数字非空格提取规则
re_score = re.compile(r'\d+')    # 数字提取规则

for each_data in datas:
    data_name = re_name.search(each_data)    # 通过正则表达式规则匹配字符串，匹配成功返回match-object
    if data_name:
        name = data_name.group(0)    # group()用来提出分组截获的字符串
    data_score = re_score.search(each_data)    # 通过正则表达式匹配字符串，匹配成功返回match-object
    if data_score:
        score = data_score.group(0)

    # 计算分数和以及次数和
    last_result = result.get(name,(0,0))    # dict.get(key, default=None)。key在dicr中存在则返回相应值，否则返回default的值
    result[name] = (last_result[0] + int(score),last_result[1] + 1)

# 对结果进行排序
# 字典(Dictionary) items() 函数以列表返回可遍历的(键, 值) 元组数组。
# key指定一个接收一个参数的函数，这个函数用于从每个元素中提取一个用于比较的关键字。此处提取的是分数。
# 若key修改为lambda x:x[1][1]，则按次数排序
# sorted_result()返回一个列表
sorted_result = sorted(result.items(),key=lambda x:x[1][0],reverse=True)
# sorted_result = sorted(result.items(),key=lambda x:x[1][1],reverse=True)    # 按次数排序

data = []
for each_result in sorted_result:
    # 将每一人的成绩格式化，同时计算平均分
    s = '%s|%d|%d|%.1f\n' % (each_result[0], each_result[1][0], each_result[1][1], float(each_result[1][0]) / each_result[1][1])
    data.append(s)

# 保存文件
with open('result.txt','w') as f:
    f.write('名字|总分|次数|平均分\n')
    f.writelines(data)
