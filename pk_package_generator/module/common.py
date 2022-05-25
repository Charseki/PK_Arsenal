# -*- coding: utf-8 -*-
import json
import re
import base64
import random
from urllib.parse import unquote
import time
import os
import string
from enum import Enum
from configparser import ConfigParser
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem, Popularity


class common():
    __cfg = None
    get_post_template = '''{method} {url} HTTP/1.1\r\nHost: {host}\r\n{otherhead}\r\n{body}'''
    user_agent_rotator = None
    paths = None
    filename = None
    hosts = None
    payload_location = None
    paramenames = None
    headers = None
    __body_cached = None
    noreapeat_name = None
    multipart_exp = None
    content_type_exp = None

    def __init__(self, cfg_path):
        self.currentpath = os.getcwd()
        self.__cfg = ConfigParser()
        self.__cfg.read(cfg_path)
        self.init_ua()
        self.init_path()
        self.init_filename()
        self.init_host()
        self.init_parame_name()
        self.init_parame_get()
        self.init_headers()

    def init_ua(self):
        israndom_ua = self.__cfg.getboolean('HTTPHEADER', 'random_ua')
        if (israndom_ua):
            random_ua_limit = self.__cfg.getint('HTTPHEADER', 'random_ua_limit')
            ua_popularity = [Popularity.COMMON.value, Popularity.POPULAR]
            self.user_agent_rotator = UserAgent(popularity=ua_popularity, limit=random_ua_limit)

    def init_path(self):
        pathfile = os.path.join(self.currentpath, "source/paths.txt")
        self.paths = json.loads(open(pathfile, "r").read())

    def init_filename(self):
        filenamefile = os.path.join(self.currentpath, "source/filename.txt")
        self.filename = json.loads(open(filenamefile, "r").read())

    def init_host(self):
        hostsfile = os.path.join(self.currentpath, "source/domains.txt")
        self.hosts = json.loads(open(hostsfile, "r").read())

    def init_parame_name(self):
        paramesfile = os.path.join(self.currentpath, "source/parame_value2.txt")
        tmp_parames = json.loads(open(paramesfile, "r").read())
        parames_dic = {}
        for k, v in tmp_parames.items():
            parames_dic[k] = [unquote(value) for value in v]
        self.paramenames = parames_dic

    def init_parame_get(self):
        paramesfile = os.path.join(self.currentpath, "source/parame_value_get.txt")
        tmp_parames = json.loads(open(paramesfile, "r").read())
        parames_dic = {}
        for k, v in tmp_parames.items():
            parames_dic[k] = [unquote(value) for value in v]
        self.paramenames_get = parames_dic

    def init_headers(self):
        headersfile = os.path.join(self.currentpath, "source/headers2.txt")
        tmp_headers = json.loads(open(headersfile, "r").read())
        headers_dic = {}
        for k, v in tmp_headers.items():
            headers_dic[k] = [unquote(value) for value in v]
        self.headers = headers_dic

    def get_random_UA(self):
        return self.user_agent_rotator.get_random_user_agent()

    def get_random_path(self):
        return random.choice(self.paths)

    def get_random_filename(self):
        filename, subfix = os.path.splitext(random.choice(self.filename))
        # 9月份规则中18010047,aspx的访问中不允许出现%,因此去掉所有aspx、asp后缀
        # subfix = random.choice(["php", "asp", "jsp", "aspx", "action", "html"])
        subfix = random.choice(["php", "jsp", "action", "html"])
        return "{}.{}".format(filename, subfix)

    def __get_url(self):
        parames = []

        __min = self.__cfg.getint("URL", "parame_num_min")
        __max = self.__cfg.getint("URL", "parame_num_max")
        parame_num = random.randint(__min, __max)
        tmp_parame = [self.noreapeat_name]
        while self.noreapeat_name in tmp_parame:
            tmp_parame = random.sample(self.paramenames_get.keys(), parame_num)
        for i in tmp_parame:
            parames.append("{}={}".format(i, random.choice(self.paramenames_get[i])))

        # 加上payload
        if self.payload_location == "url_parame":
            parames.append(self.payload)
            parame_num += 1

        if parame_num != 0:
            random.shuffle(parames)
            parames_str = "?" + "&".join(parames)
        else:
            parames_str = ""

        file_name = self.payload if self.payload_location == 'file_name' else self.get_random_filename()

        res_url = "/{}/{}{}".format(self.get_random_path(), file_name, parames_str)
        return res_url

    def get_random_host(self):
        return random.choice(self.hosts)

    def __get_otherhead(self, header: list = None, body: list = None):
        '''

        :param header: 预定义头,list类型
        :return:
        '''

        if header != None:
            headers = header
            headers_num = len(headers)
        else:
            headers = []

            __min = self.__cfg.getint("HEADERS", "headers_num_min")
            __max = self.__cfg.getint("HEADERS", "headers_num_max")

            headers_num = random.randint(__min, __max)
            tmp_headers_key = random.sample(self.headers.keys(), headers_num)
            for i in tmp_headers_key:
                tmp_headers_value = random.choice(self.headers[i])
                headers.append("{}: {}".format(i, tmp_headers_value))

        # 加上payload
        if (self.payload_location == "other_head"):
            headers.append(self.payload)
            headers_num += 1

        if (self.method == "POST"):
            # Content-Type
            if self.encoding == 'multipart':
                if self.multipart_exp is None:
                    self.multipart_boundary = '----WebKitFormBoundary{}'.format(''.join(
                        random.sample(string.ascii_letters + string.digits, random.randint(4, 10))))
                else:
                    self.multipart_boundary = self.multipart_exp
                if self.content_type_exp is None:
                    headers.append('Content-Type: multipart/form-data; boundary={}'.format(self.multipart_boundary))
                else:
                    headers.append(self.content_type_exp)
            else:
                headers.append('Content-Type: application/x-www-form-urlencoded')

            # 加上Content-length头
            length = len(self.__get_body(body))
            headers.append("Content-length: {}".format(length))
            headers_num += 1
            self.__get_body()

        if (headers_num != 0):
            random.shuffle(headers)
            headers_str = "\r\n".join(headers)
            headers_str += "\r\n"
        else:
            headers_str = ""
        return headers_str

    def __get_body(self, body: list = None):
        # 使用缓存机制,先于Content-Length生成body,但如果多线程,这里就会出逻辑问题
        if (self.__body_cached != None):
            return self.__body_cached

        if (self.method == "GET"):
            self.__body_cached = ""
            return ""

        if body != None:
            parame_num = len(body)
        else:
            body = []
            __min = self.__cfg.getint("BODY", "parame_num_min")
            __max = self.__cfg.getint("BODY", "parame_num_max")

            parame_num = random.randint(__min, __max)
            tmp_parame = [self.noreapeat_name]
            while self.noreapeat_name in tmp_parame:
                tmp_parame = random.sample(self.paramenames.keys(), parame_num)
            for i in tmp_parame:
                if self.encoding == 'multipart':
                    body.append((i, random.choice(self.paramenames[i])))
                else:
                    body.append("{}={}".format(i, random.choice(self.paramenames[i])))

        # 加上payload
        if (self.payload_location == "body_parame"):
            body.append(self.payload)
            parame_num += 1

        # 编码截阶段
        if (parame_num != 0):
            random.shuffle(body)
            if self.encoding == 'multipart':
                body_str = []
                for i in body:
                    if not isinstance(i, tuple):
                        mutidata = 'Content-Disposition: form-data; {}\r\n'.format(i)
                    else:
                        mutidata = 'Content-Disposition: form-data; name="{}";\r\n\r\n{}\r\n'.format(i[0],
                                                                                                     i[1])
                    body_str.append(mutidata)
                body_str = '--{}\r\n'.format(self.multipart_boundary).join(body_str)
                body_str = '--{line}\r\n{body}--{line}--'.format(line=self.multipart_boundary, body=body_str)
            else:
                body_str = "&".join(body)
        else:
            body_str = ""

        self.__body_cached = body_str
        return body_str

    def get_random_parame(self):
        # 先补丁,以后再改插件
        res = random.choice(list(self.paramenames.keys()))
        res = (res, random.choice(self.paramenames[res]))
        return res

    def generate(self, payload, method="GET", payload_location="get_parame", url=None, header=None, host=None,
                 body=None, encoding=None, noreapeat_name=None):
        self.method = method
        self.payload_location = payload_location
        self.payload = payload
        self.encoding = encoding
        self.noreapeat_name = noreapeat_name

        request_data = self.get_post_template
        data = {
            "method": method,
            "url": url if url else self.__get_url(),
            "host": host if host else self.get_random_host(),
            "otherhead": self.__get_otherhead(header, body),
            "body": self.__get_body(body)
        }
        request_data = request_data.format(**data)

        # 清空body缓存
        self.__body_cached = None
        return request_data

    # 兼容之前的插件,加入之前的函数
    # 关键字随机替换
    def change_keyword(self, template, keyword, keywords):
        template = template.replace(keyword, keywords[random.randint(0, len(keywords) - 1)])
        return template

    # 将关键字随机替换大小写
    def change_case(self, template, keywords):
        for keyword in keywords:
            new_keyword = ''
            for c in keyword:
                if random.randint(0, 9) % 2:
                    c = c.upper()
                else:
                    c = c.lower()
                new_keyword = '%s%s' % (new_keyword, c)
            template = template.replace(keyword, new_keyword)
        return template

    # 替换NUM 和 STR为随机
    def replace(self, template, tag, max_len, min_len=2):
        for num in range(0, len(re.findall(tag, template))):
            # 为了避免waf的一些特殊情况,随机字符个数从2开始
            max_len = random.randint(min_len, max_len)
            new_str = ''
            for x in range(0, max_len):
                if tag == 'NUM':
                    new_str = '%s%d' % (new_str, random.randint(1, 9))
                else:
                    new_str = '%s%s' % (
                        new_str, random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))
            template = template.replace(tag, new_str, 1)

            if tag == 'BASE64':
                payload = self.ramdonstr(max_len)
                payload = base64.b64encode(payload.encode("utf-8")).decode("utf-8")
                template = template.replace('BASE64', payload)
        return template

    def ramdonstr(self, max_len):
        new_str = ''
        for x in range(0, max_len):
            new_str = '%s%s' % (new_str, random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))
        return new_str
# now = time.time()
# a = common()
# print(time.time()-now)
# now = time.time()
# for i in range(1):
# print(a.generate("sss","POST"))
# print(time.time()-now)
