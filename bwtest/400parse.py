#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------
# File Name          :400parse.py
# Date               :2021/11/23 22:26:25
# Author             :Charseki.Chen
# Email              :chenshengkai@vip.qq.com
# Version            :V1.0.0
# Description        :400parse
# --------------------------------------------------

import pathlib

basedir = pathlib.Path().cwd()
outfile = basedir.joinpath('bwtest','result','new_black_6824.json')
newfile = basedir.joinpath('bwtest','result','new11111_black_6824.json')
def parse():
    with open(newfile,'w') as fw:
        with open(outfile) as f:
            for line in f.readlines():
                pos1 = line.find("GET")
                len = 3
                if pos1 == -1:
                    pos1 = line.find("POST")
                    len = 4
                if pos1 == -1: 
                    fw.write(line)
                    continue

                pos2 = line.find("HTTP/1")
                start = line[:pos1+len+1]
                end = line[pos2-1:]
                mid = line[pos1+len+1:pos2-1]
                mid = mid.replace(" ","%20")
                newline = " ".join((start, mid, end))
                fw.write(newline)

if __name__ == '__main__':
    parse()