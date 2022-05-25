import re
import argparse
from module.utils import color_print
from module.calc_time import calc_time
from urllib.parse import unquote
import json


def write_to_file(file_name: str, data: list, append=False):
    content = []
    if (append):
        try:
            with open(file_name, "r") as file:
                content = json.loads(file.read())
        except Exception as e:
            print(e)
    content = set(content)
    content |= set(data)
    content = list(content)
    with open(file_name, "w") as file:
        file.write(json.dumps(content, indent=4))


def write_to_file_dic(file_name: str, data: dict, append=False):
    content = {}
    if (append):
        try:
            with open(file_name, "r") as file:
                content = json.loads(file.read())
        except Exception as e:
            print(e)
    for i in data:
        content[i] = set(content.setdefault(i, []))
        content[i] |= set(data.setdefault(i, []))
        content[i] = list(content[i])
    with open(file_name, "w") as file:
        file.write(json.dumps(content, indent=4))


def make_domains(data):
    result = set()

    # 匹配HOST中的域名
    re_pattern = re.compile('''Host%3A%20(([a-zA-Z0-9]+\.)+[a-zA-Z0-9]+)%0D%0A''')
    for i in re_pattern.findall(data):
        tmp = i[0]
        result.add(tmp)
    result = list(result)
    write_to_file("./source/domains.txt", result, append=False)


def make_paths(data):
    result = set()

    # 匹配url中的路径名
    re_pattern = re.compile('''%20/([a-zA-Z/]+)/''')
    for i in re_pattern.findall(data):
        tmp = i
        if len(tmp)>50:continue
        result.add(tmp)

    result = list(result)
    write_to_file("./source/paths.txt", result, append=False)


def make_filename(data):
    result = set()

    # 匹配url中的文件名
    re_pattern = re.compile('''/([a-zA-Z0-9_]+)\.([a-zA-Z0-9]+)%20HTT''')

    for i in re_pattern.findall(data):
        tmp = ".".join(i)
        if tmp.lower().find('spy')!=-1:continue
        if tmp.lower().find('shell')!=-1:continue
        result.add(tmp)

    result = list(result)
    write_to_file("./source/filename.txt", result, append=False)


def make_parame_value(data):
    '''
    从json文件中提取参数键和值
    :param data: 原始数据包json文件
    :return: 在指定目录下创建parame_value.txt
    '''
    result = {}
    ignore = ['aid','info','millis']
    # get参数处理
    re_pattern = re.compile('''%3F(.*?)%20HTTP/1''')
    for parames in re_pattern.findall(data):
        for p in parames.split('%26'):
            tmp = p + '%3D'
            tmp = tmp.split('%3D')
            # tmp = "{}:{}".format(tmp[0],tmp[1])
            if tmp[0] in ignore:
                continue
            result.setdefault(tmp[0], set()).add(tmp[1])

    #  旧的参数匹配方式,不全,当只有一个post参数时无法匹配
    # # post第一个参数
    # re_pattern = re.compile('''%0D%0A%0D%0A([_a-z][_a-zA-z0-9]*?)%3D(.*?)(%26|%0D%0A)''')
    #
    # for i in re_pattern.findall(data):
    #     if i[1].find("%20") != -1: continue
    #     # tmp = "{}:{}".format(i[0], i[1])
    #     if i[0] in ignore:
    #         continue
    #     result.setdefault(i[0], set()).add(i[1])
    #
    # # post其他参数
    # re_pattern = re.compile('''%0D%0A%0D%0A(.*%26([_a-zA-Z][_a-zA-z0-9]*?)%3D(.*?)(%26|%0D%0A|%20HTTP))''')
    #
    # for i in re_pattern.findall(data):
    #     if i[2].find("%20") != -1: continue
    #     # tmp = "{}:{}".format(i[1], i[2])
    #     if i[1] in ignore:
    #         continue
    #     result.setdefault(i[1], set()).add(i[2])

    # 临时使用,只对非multipart做了处理
    for line in data.split('\n'):
        if len(line) < 5: continue
        if line.find(":")!=-1:
            data = line.split(":")[1]
        data = data.strip().strip(',').strip('"')
        post_body =data.find("%0D%0A%0D%0A")
        if post_body==-1:continue
        post_body = data[post_body+12:]
        parames = post_body.split("%26")
        for parame in parames:
            equal = parame.find("%3D")
            if equal==-1:continue
            key,value = parame[:equal],parame[equal+3:]
            result.setdefault(key, set()).add(value)

    for k in result.keys():
        result[k] = list(result[k])
    write_to_file_dic("./source/parame_value.txt", result, append=False)


def make_header(data):
    result = {}
    hd_set=set()
    abort_list = ["Cookie", "Host", "Content-Length",'Content-Type','info']
    abort_list = [i.lower() for i in abort_list]
    re_pattern = re.compile('''%0D%0A([a-zA-Z_-]+?)%3A%20([a-zA-Z%0-9-_\.]+?)%0D%0A''')
    for i in re_pattern.findall(data):
        if i[0].lower() in hd_set:continue
        if i[0].lower() in abort_list: continue
        result.setdefault(i[0], set()).add(i[1])
        hd_set.add(i[0].lower())
    for i in result:
        result[i] = list(result[i])
    write_to_file_dic("./source/headers.txt", result, append=False)


def start():
    parser = argparse.ArgumentParser(
        description='[*] 生成器source素材提取工具',
        epilog='[*] 例如:\n[*] usage: python3 ./source_generator.py -f ./data_predeal/intersection.json',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('-f', '--file', action='store', help='读取原文件路径(json格式)',
                        default="./data_predeal/Union.json")

    args = parser.parse_args()
    t = calc_time()
    with open(args.file) as file:
        data = file.read()
    function_dict = {
        "domains.txt": make_domains,
        "paths.txt": make_paths,
        "filename.txt": make_filename,
        "parame_value.txt": make_parame_value,
        "headers.txt": make_header
    }

    t.get_diff_time()
    for fname, func in function_dict.items():
        color_print("正在生成{}...".format(fname), "blue")
        func(data)
        color_print("完成,用时{}".format(t.get_diff_time()), "greenbold")


if __name__ == '__main__':
    start()
