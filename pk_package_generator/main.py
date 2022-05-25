#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
import random
from urllib.parse import quote
import argparse
import importlib
from module.utils import color_print
from module import utils, common

# MODULE_VERSION = ""
# 切换为2022052001版本插件库
MODULE_VERSION = "_2022052001"

class generator:
    # 2022.05.20 白样本插件测试情况
    white_module = ['phpmyadmin','sql','fileupload','vul_error']
    white_module_percentage = [100//len(white_module)]*len(white_module)
    # 2022.05.20 黑样本插件测试情况
    # black_module = ['codeinject','fileupload','filedownload','fileinclude','cross_path','csrf','ssrf','cves','javainject','javaunserialize','nsfocus_xss','scaner','sensitive_info','sql']
    black_module = ['fileupload','filedownload','fileinclude','cross_path','csrf','ssrf','javainject','javaunserialize','sql']
    black_module_percentage = [100//len(black_module)]*len(black_module)

    white_module_obj = {}
    black_module_obj = {}

    packages = []

    common = None

    def __init__(self):
        for module_name in self.white_module:
            self.white_module_obj[module_name] = (
                importlib.import_module("module.white{}.{}".format(MODULE_VERSION, module_name)))
        for module_name in self.black_module:
            self.black_module_obj[module_name] = (
                importlib.import_module("module.black{}.{}".format(MODULE_VERSION, module_name)))

    def load_data(self):
        self.common = common.common("./config.ini")

    def __random_group(self, amount, group_num):
        '''
        随机分组
        :param amount: 总条目数
        :param group_num: 需要分成几组
        :return: 分组后每组条目数
        '''
        point = []
        for _ in range(group_num - 1):
            point.append(random.randint(0, amount))
        point.append(0)
        point.append(amount)
        point.sort()
        res = []
        for i in range(len(point))[1:]:
            res.append(point[i] - point[i - 1])
        return res

    def __get_group(self, amount, group_num, isblack=True):
        percentage_list = self.black_module_percentage if isblack else self.white_module_percentage
        if len(percentage_list) != group_num:
            raise Exception("percentage list ERROR")
        group_result = [int(amount * i) // 100 for i in percentage_list]
        group_result[-1] = amount - sum(group_result[:-1])
        return group_result

    def __equal_group(self, amount, group_num):
        '''
        等额分组,没办法整除的最后一组会多几条
        :param amount: 总条目数
        :param group_num: 需要分成几组
        :return: 分组后每组条目数
        '''
        every_amount = amount // group_num
        return [every_amount] * (group_num - 1) + [amount - (every_amount * (group_num - 1))]

    def __print_module_msg(self, module_list, amount_array, is_white=True):
        color_print("已启用{}名单插件 {}".format("白" if is_white else "黑", ",".join(module_list)), "yellowbold")
        start = 0
        for i, num in enumerate(amount_array):
            color_print("{}-{}\t\t{} 插件".format(start, start + num - 1, module_list[i]), "yellowbold")
            start += num

    def generate_white_package(self, amount):
        if amount == 0: return
        # amount_array = self.__random_group(amount, len(self.white_module))
        amount_array = self.__get_group(amount, len(self.white_module), False)
        self.__print_module_msg(self.white_module, amount_array)
        for i, module in enumerate(self.white_module_obj.values()):
            class_object = getattr(module, self.white_module[i])
            self.packages += class_object(self.common).generate_packages(amount_array[i])

    def generate_black_package(self, amount):
        if amount == 0: return
        # amount_array = self.__random_group(amount, len(self.black_module))
        amount_array = self.__get_group(amount, len(self.black_module), True)
        self.__print_module_msg(self.black_module, amount_array, False)
        for i, module in enumerate(self.black_module_obj.values()):
            class_object = getattr(module, self.black_module[i])
            self.packages += class_object(self.common).generate_packages(amount_array[i])

    def save_package(self, file_name, append=False):
        '''
        转换为字典,url编码后保存
        '''
        content = {}
        if (append):
            try:
                with open(file_name, "r") as file:
                    content = json.loads(file.read())
            except Exception as e:
                print(e)
        content = content.values()

        # 去重,感觉没必要,21.11.01改为不去重
        # content = set(content)
        # content |= set(self.packages)

        content = list(content)
        content += self.packages

        content = {num: quote(v) for num, v in enumerate(content)}
        with open(file_name, "w") as file:
            file.write(json.dumps(content, indent=4))

    def single_payload_package(self, options):
        from module import special_test
        sp = special_test.special_test(self.common)
        self.packages += sp.generate_packages(options)

    def start(self):
        parser = argparse.ArgumentParser(
            description='[*] 长亭绕过、误报样本生成工具',
            epilog='[*] 例如:\n[*] usage: python3 ./main.py/ -w 4000 -b 1000\n[*] 执行完成后会:\n[*] 在 f_white_fn.json 追加白样本(误报样本)4000个\n[*] 在 f_black_fn.json 追加黑样本(绕过样本)1000个',
            formatter_class=argparse.RawTextHelpFormatter
        )

        parser.add_argument('-s', '--special', action='store', help='header,parame', default=None)
        parser.add_argument('-w', '--white', action='store', help='输入数字，白样本(误报样本)数量', default=0)
        parser.add_argument('-b', '--black', action='store', help='输入数字，黑样本(绕过样本)数量', default=0)
        parser.add_argument('-o', '--output', action='store', help='输出json样本位置,默认为./output/sample.json',
                            default="./output/sample.json")
        args = parser.parse_args()

        white_num = int(args.white)
        black_num = int(args.black)

        if (not (white_num or black_num or args.special != None)):
            parser.print_help()
            exit()

        color_print("[*] 正在加载数据,初始化生成器...", "blue")
        self.load_data()
        color_print("[*] 数据加载完成", "green")
        color_print("[*] 开始生成数据包...", "blue")

        if (args.special != None):
            sp_args = args.special.split(",")
            rst = []
            for op in self.special_allow_method:
                if op in sp_args:
                    rst.append(op)
            color_print("识别到{},参数正确".format(",".join(rst)), "greenbold")
            self.single_payload_package(rst)
        else:
            color_print("[*] 开始生成数据包...", "white")
            self.generate_white_package(white_num)
            self.generate_black_package(black_num)

        color_print("[*] 生成完成,开始写入数据...", "blue")
        self.save_package(args.output)


if __name__ == '__main__':
    generator().start()