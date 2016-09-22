#-*- coding:utf-8 -*-

import os

class FindFile(object):

    def find_file(self,sensitive_word,file_directory='.'):
        """
        在文件目录中查找关键字，若未输入目录则默认为查找当前目录
        :param sensitive_word:敏感字
        :param file_directory:查找目录，默认为当前目录
        :return:
        """
        results = []
        # os.walk()遍历文件目录，返回一个三元元组(dirpath,dirnames,filenames)，分别对应起始路径，起始路径下的文件目录，起始路径下的文件
        # dirpath是一个string，代表目录的路径.
        # dirnames是一个list，包含了dirpath下所有子目录的名字,
        # filenames是一个list，包含了非目录文件的名字.这些名字不包含路径信息,如果需要得到全路径,需要使用 os.path.join(dirpath, name).
        for dirpath,dirnames,filenames in os.walk(file_directory):
            # print('正在%s查找%s...' % (dirpath,sensitive_word))
            for each_name in filenames:
                full_name = dirpath + '/' + each_name    # 配置文件路径
                if sensitive_word in full_name:    # 检查敏感字是否在文件路径中
                    results.append(full_name)    # 文件名中存在敏感词，则将文件路径添加到结果列表中
                # 检查文件内容中是否包含敏感词
                with open(full_name,'r') as f:
                    datas = f.readlines()
                    for each_data in datas:
                        if sensitive_word in each_data:    # 检查文件内容中是否存在敏感词
                            results.append(full_name + ":" + each_data)    # 检查存在敏感词，则将当前行的内容保存到结果列表中
        return results

    def main(self):
        """
        main函数，主函数，获取用户输入信息
        :return:
        """
        sensitive_word = raw_input('请输入敏感词：')
        file_directory = raw_input('请输入查找目录：')
        if not file_directory:
            file_directory = '.'
        search_result = self.find_file(sensitive_word,file_directory)

        print('\n' + '=' * 20 + ' result ' + '=' * 20 + '\n')
        for each_result in search_result:
            print each_result

if __name__ == '__main__':
    ff = FindFile()
    ff.main()