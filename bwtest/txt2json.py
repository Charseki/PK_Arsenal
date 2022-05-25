#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------
# File Name          :txt2json.py
# Date               :2021/08/31 16:54:10
# Author             :Charseki.Chen
# Email              :chenshengkai@vip.qq.com
# Version            :V1.0.0
# Description        :*.txt 2 json for bwtest
# --------------------------------------------------

#!/usr/bin/env python
# coding=utf-8

import os
import json
import pathlib

BaseDir = pathlib.Path(os.getcwd())


# 读文件
def readfile(filename):
    content = ''
    with open(filename, 'r') as f:
        content = f.read()
    return content


# 写文件
def writefile(filename, content):
    with open(filename, 'w') as f:
        f.write(content)


# 列文件保存到files
def listdir(path, files):
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            listdir(filepath, files)
        else:
            files.append(filepath)


def main():
    # 获取所有txt保存到txtfiles
    txtfiles = []
    listdir(BaseDir.joinpath('bwtest','OutputFile/'), txtfiles)

    output = dict()
    # 生成json
    for x in txtfiles:
        if '.DS_Store' in x:
            continue
        if os.path.exists(x):
            key = os.path.basename(x).split('.')[0]
            output[key] = readfile(x)

    # 格式化json字符串
    output = json.dumps(output, indent=4)

    # 保存json字符串到out.json文件
    file_name = 'new_white_9007'
    writefile(BaseDir.joinpath('bwtest','result',f'{file_name}.json'), output)


print('------ *.txt合并成json文件成功 ------')
print('-------------------------------------')

if __name__ == '__main__':
    main()
