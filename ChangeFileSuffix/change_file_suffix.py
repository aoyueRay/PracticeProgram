#-*- coding:utf-8 -*-

import os

files = os.listdir('.')    # 列出当前目录下的所有文件
for each_file in files:
    name_suffix = os.path.splitext(each_file)    # os.path.splitext(path)分割路径，返回路径名和文件扩展名的元组
    if name_suffix[1] == '.pdf':    # 若后缀为pdf，则定义新文件名为avi后缀
        new_name  = name_suffix[0] + '.avi'
        os.rename(each_file,new_name)    # os.rename(old,new)将旧文件名重命名为新文件名