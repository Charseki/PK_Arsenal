# -*- coding:utf-8 -*-

import urllib.parse
import argparse
from module.http_repeater import http_repeater
import platform

if platform.platform().find('Windows') != -1:
    from module.utils import color_print_win as color_print
else:
    from module.utils import color_print


def help():
    parser = argparse.ArgumentParser(
        description=color_print('用来对WAF进行FUZZ测试的一个工具', "blue"),
        epilog=color_print('[*] usage: python main.py -u http://127.0.0.1:80 -i ./data/example.json -t 50 --timeout 10',
                           "blue"),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('-u', '--url', action='store', help="测试站点的URL或者IP", default=None, required=True)
    parser.add_argument('-p', '--port', action='store', type=int, default=80, help="保护目标的端口")
    parser.add_argument('-t', '--thread', action='store', type=int, default=5, help='发送数据的线程数，默认为5')

    data_source_group = parser.add_mutually_exclusive_group(required=True)
    data_source_group.add_argument('-i', '--input', action='store', default='./data/samples.json',
                                   help="传输的包文,默认使用json目录下的samples.json")
    data_source_group.add_argument('-s', '--sql', action='store_true', help="数据包来源为sql,从config.ini读取配置")

    parser.add_argument('--timeout', action='store', type=int, default=5, help="超时时间，默认为5")
    parser.add_argument('--proxy', action='store', default=None, help="设置HTTP代理(--proxy 127.0.0.1:8080)")
    parser.add_argument('--host', action='store', default=None, help="设置Host字段(用于需要指定Host的场景,如:玄武盾)")


    parser.add_argument('--start', action='store', default=0, help="包起始编号")
    parser.add_argument('--end', action='store', default=0, help="包结束编号")
    parser.add_argument('-o', '--output', action='store', default=None, help="输出文件路径,默认不输出")

    args = parser.parse_args()

    start = int(args.start)
    end = int(args.end)
    output = args.output

    if not args.url:
        color_print('[*] 必须设置目标URL,如: - http://test.ngwdev.com/', 'red')
        exit()
    if args.url.startswith(r'http://') or args.url.startswith(r'https://'):
        p = urllib.parse.urlparse(args.url)
        if p.hostname:
            args.url = p.hostname
        if p.port:
            args.port = int(p.port)
    if args.sql:
        args.input = None
    repeater = http_repeater(args.url, args.port, args.input, args.thread, args.timeout, proxy=args.proxy,host=args.host)
    repeater.start_to_fuzz(output, start=start, end=end)


if __name__ == '__main__':
    help()
