#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys


def prettyprint(l):
    if not 'indentation' in prettyprint.__dict__:
        indentation = prettyprint.__dict__['indentation'] = ''
    else:
        indentation = prettyprint.__dict__['indentation']

    print('{}['.format(indentation))

    for i in l:
        if isinstance(i, list) and filter(lambda x: isinstance(x, list), i):
            prettyprint.__dict__['indentation'] = '{}    '.format(indentation)
            prettyprint(i)
            prettyprint.__dict__['indentation'] = indentation
        else:
            print('    {}{}'.format(indentation, i))

    print('{}]'.format(indentation))

    if prettyprint.__dict__['indentation'] == '':
        del prettyprint.__dict__['indentation']


def random_bytes(length):
    if length == 0:
        return ""

    return open('/dev/urandom', 'rb').read(length)


def red(s):
    return '\033[31m{}\033[0m'.format(s)


def blue(s):
    return '\033[34m{}\033[0m'.format(s)


def green(s):
    return '\033[92m{}\033[0m'.format(s)


def yellow(s):
    return '\033[93m{}\033[0m'.format(s)


def bold(s):
    """
    加粗
    :param s:
    :return:
    """
    return '\033[1m{}\033[21m'.format(s)


def redbold(s):
    return red(bold(s))


def bluebold(s):
    return blue(bold(s))


def greenbold(s):
    return green(bold(s))


def yellowbold(s):
    return yellow(bold(s))


def color_print(content, color):
    color_list = ["", "red", "blue", "green", "yellow"]
    font_list = ["bold"]
    func_list = color_list + font_list + ["{}{}".format(i, j) for i in color_list for j in font_list]
    if (color in func_list):
        __print(eval(color)(content))

def color_print_win(content, color):
    # windows cmd不支持彩色输出,直接忽略color
    __print(content)


def __print(content):
    sys.stdout.write(content + "\n")
    sys.stdout.flush()
