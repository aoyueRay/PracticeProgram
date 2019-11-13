# -*- coding:utf-8 -*-

# import area
import jieba.analyse
from collections import Counter


# class area
class AnnualPlan(object):

    def __init__(self):
        pass


    def plan_2019(self):

        # 打开文件
        with open('annual.txt', 'r') as f:
            contents = f.read()

        result_counter = jieba.cut(contents, cut_all=True)
        # result_counter = jieba.analyse.extract_tags(contents, topK=100, withWeight=False)
        result = Counter(result_counter)

        # 字典排序
        final_result = sorted(result.items(), key=lambda item: item[1], reverse=True)

        with open('result.txt', 'w') as f:
            for each in final_result:
                str_each = each[0].encode('utf-8') + '|' + str(each[1]) + '\n'
                f.write(str_each)

        # result = jieba.analyse.extract_tags(contents, topK=100,withWeight=True)

    def requirements_2019(self):

        # 打开文件
        with open('123.txt', 'r', encoding='gbk') as f:
            contents = f.read()

        result_counter = jieba.cut(contents, cut_all=True)
        # result_counter = jieba.analyse.extract_tags(contents, topK=100, withWeight=False)
        result = Counter(result_counter)

        # 字典排序
        final_result = sorted(result.items(), key=lambda item: item[1], reverse=True)

        with open('result.txt', 'w') as f:
            for each in final_result:
                str_each = each[0] + '|' + str(each[1]) + '\n'
                f.write(str_each)

        # result = jieba.analyse.extract_tags(contents, topK=100,withWeight=True)



# main area
if __name__ == '__main__':
    ap = AnnualPlan()
    ap.requirements_2019()
