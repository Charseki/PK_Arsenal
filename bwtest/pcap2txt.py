#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------
# File Name          :pcap2txt.py
# Date               :2021/08/31 10:43:32
# Author             :Charseki.Chen
# Email              :chenshengkai@vip.qq.com
# Version            :V1.0.0
# Description        :pcap2txt
# --------------------------------------------------

import pathlib
import os


# 变量定义
txt_file_name = 'black_02_packet_details.txt'
BaseDir = pathlib.Path().cwd()
old_inputfile_path = BaseDir.joinpath('bwtest','InputFile',txt_file_name)
new_inputfile_path = BaseDir.joinpath('bwtest','InputFile',f'new_{txt_file_name}')
outputfile_path = BaseDir.joinpath('bwtest','OutputFile')
num = 1
total = 0
# 从pcapxray结果中过滤出GET和POST请求
get_post_cmd = os.system(f'cat {old_inputfile_path} | grep GET > {new_inputfile_path} && cat {old_inputfile_path} | grep POST >> {new_inputfile_path}')
# 开始过滤
with open(new_inputfile_path) as f:
    for line in f.readlines():
        # 第一次过滤
        line_1 = line.replace('        ','').replace('\"b\'','').replace('\"b\\\"','').replace('\'\",','').replace('\\\\','\\').replace('\\\"','\"').replace('\\\'','\'')
        # 第二次过滤
        line_2 = line_1.replace('\\\\','\\').replace('\\r\\n','\n').replace('\\n','\n')
        total +=1
        with open(outputfile_path.joinpath(str(num) + '.txt'),'w') as ft:
            ft.write(line_2)
            num += 1
            print('\n------- Task End ! 总共提取{}条请求报文 -------'.format(total))