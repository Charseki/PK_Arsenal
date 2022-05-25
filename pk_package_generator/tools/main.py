# -*- coding:utf-8 -*-

import json
import argparse
from lib.json_merge import merge
from lib.json_diff import diff
from lib.json_cut import cut
import lib.utils
import lib.json_cut
import lib.json_diff


def main():
    parser = argparse.ArgumentParser(
        description=lib.utils.blue('JSON处理工具'),
        epilog=lib.utils.blue('[*] usage: python json_cut.py -f samples.json -o out.json -n 1000'),
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers()

    parse_cut = subparsers.add_parser('cut', help="json剪切")
    parse_cut.add_argument('-f', '--file', action='store', help="原JSON文件", required=True)
    parse_cut.add_argument('-n', '--maxlinenum', action='store', help="剪切条目", required=True)
    parse_cut.add_argument('-o', '--output', action='store', default='out.json', help="输出JSON文件")
    parse_cut.set_defaults(func=cut)

    parse_diff = subparsers.add_parser('diff', help="json对比")
    parse_diff.add_argument('-a', '--jsonfile1', action='store', help="输入JSON文件1", required=True)
    parse_diff.add_argument('-b', '--jsonfile2', action='store', help="输入JSON文件1", required=True)
    parse_diff.add_argument('-o', '--outpath', action='store',
                            help="输出目录,将在该目录下输出 a&b, a|b, a-(a&b), b-(a&b), 四个文件",
                            default='./data/')
    parse_diff.set_defaults(func=diff)

    parse_merge = subparsers.add_parser('merge', help="json合并")
    parse_merge.add_argument('-p', '--json_path', action='store', help='原文件路径', required=True)
    parse_merge.add_argument('-s', '--subfix', action='store', help='合并的文件后缀', required=True)
    parse_merge.add_argument('-o', '--outfile', action='store', default='./data/out.json', help='输出JSON文件')
    parse_merge.set_defaults(func=merge)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
