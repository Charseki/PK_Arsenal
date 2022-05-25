# -*- coding:utf-8 -*-

import time
import re
import platform
import json
import socket
import os
from configparser import ConfigParser
from urllib.parse import unquote, quote
from xml.sax.saxutils import unescape
from multiprocessing.dummy import Pool as ThreadPool

if platform.platform().find('Windows') != -1:
    from .utils import color_print_win as color_print
else:
    from .utils import color_print


class http_repeater:
    unique_id_num = 1000000
    every_saved_packages = 100
    response_code_package = {}
    response_code_num = {}
    package = None
    __cfg = None
    max_retry = 5

    # 该变量记录原始包的损坏情况
    fixed_package = []
    savepath = None

    rep_host = re.compile(r'Host: [^\r\n]*\r\n')

    code_event = {'000': "返回包格式不正确",
                  '111': "连接超时",
                  '112': "经过修复后才正常",
                  '200': "正常访问(200)",
                  '403': "Forbiden(403)",
                  '404': "页面不存在(404)",
                  '500': "服务器出错(500)",
                  '900': "特别记录"
                  }
    collection_code = []

    def __init__(self, target_ip, target_port, input_data, thread, timeout, proxy=None, host=None):
        self.target_ip = target_ip
        self.target_port = target_port
        self.load_config(input_data)
        self.max_thread = thread
        self.timeout = float(timeout)
        if host:
            self.host = "Host: {}\r\n".format(host)
        else:
            self.host = None
        if proxy:
            self.set_proxy(proxy)

    def pre_deal_BOM(self):
        bom_char = b"\xEF\xBB\xBF"
        with open("config.ini", "rb") as cfg:
            content = cfg.read()
        if content[:3] != bom_char: return
        content = content[3:]
        with open("config.ini", "wb") as cfg:
            cfg.write(content)
            color_print("成功预处理BOM头", "greenbold")

    def load_config(self, input_data):
        color_print("[*] 开始加载数据...", 'blue')
        self.__cfg = ConfigParser()
        cfg_path = 'config.ini'
        if not os.path.exists(cfg_path):
            color_print("加载错误,config.ini不存在", "redbold")
            color_print("请先配置config.ini,选项可参考config.ini.bak", "redbold")
            exit()
        self.pre_deal_BOM()
        self.__cfg.read(cfg_path, encoding='utf8')

        # 请求数据加载
        if input_data != None:
            self.fromsql = False
            self.load_file(input_data)
        else:
            self.fromsql = True
            self.load_sql()

        # 请求结果配置
        tmp_config = self.__cfg.get('RESULT', 'record_status')
        tmp_config = tmp_config.split(',')
        tmp_config = [i.strip() for i in tmp_config]
        self.collection_code = tmp_config

        tmp_config = self.__cfg.getint('RESULT', 'every_saved_packages')
        self.every_saved_packages = tmp_config

        tmp_config = self.__cfg.getint('RESULT', 'timeout_retry')
        self.max_retry = tmp_config

        color_print("[*] 数据加载完成", 'green')

    def set_proxy(self, proxy):
        import socks
        proxy = proxy.strip()
        proxy_ip, proxy_port = proxy.split(":")
        socks.set_default_proxy(socks.HTTP, proxy_ip, int(proxy_port))
        socket.socket = socks.socksocket

        # 测试代理
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            s.connect((self.target_ip, self.target_port))
            color_print("连接代理地址{}:{}成功".format(proxy_ip, proxy_port), "greenbold")
        except TimeoutError as e:
            color_print("{}".format("连接超时,建议修改超时时长或检查代理地址"), "red")
            raise e

    def load_sql(self):
        import pymysql as mdb
        query_db_name = 'fix_packages'
        query_conn = mdb.connect(
            host=self.__cfg.get('SQL', 'host'),
            user=self.__cfg.get('SQL', 'user'),
            passwd=self.__cfg.get('SQL', 'pass'),
            db=self.__cfg.get('SQL', 'query_database'),
            port=self.__cfg.getint('SQL', 'port'),
            charset='utf8'
        )
        cur = query_conn.cursor(mdb.cursors.DictCursor)
        sql = 'select package from packages'
        cur.execute(sql)
        rows = cur.fetchall()
        self.package = {num: dic["package"] for num, dic in enumerate(rows)}
        cur.close()

    def load_file(self, file):
        request_text = open(file).read()
        data = json.loads(request_text)
        if isinstance(data, list):
            self.package = {num: pkg for num, pkg in enumerate(data)}
        else:
            self.package = data

    def get_unique_id(self):
        timestamp = int(time.time())
        self.unique_id_num += 1
        return "{}{}".format(timestamp, self.unique_id_num)

    def add_info(self, package, unique_id):
        found = re.findall(r'Content-Length: [\d]+?\r\n', package, re.IGNORECASE)
        if found:
            found = found[0]
            package = package.replace(found, '{}repeat-id: {}\r\n'.format(found, unique_id))
        return package

    def fix_package(self, package: str):
        # 修复算法
        package = ''.join(['\r%s' % package[x] if package[x] == '\n' and package[x - 1] != '\r' else package[x] for x in
                           range(0, len(package))])
        pos = package.find('\r\n\r\n')
        if pos != -1:
            length = len(package) - pos - 4
        else:
            package = package.rstrip('\r').rstrip('\n').rstrip()
            pos = len(package)
            # 修复请求包
            package = '%s\r\n\r\n' % package
            length = 0
        # 填充Content-Length
        found = re.findall(r'\bContent-Length[\s]*:[\S\s]+?\r\n', package, re.IGNORECASE)
        if len(found) > 0:
            found = found[0]
            package = package.replace(found, 'Content-Length: %d\r\n' % length)
        else:
            package = '%s%s%s' % (package[0: pos], '\r\nContent-Length: %d' % length, package[pos:])
        return package

    def socket_repeat(self, id, repeat_txt):
        repeat_txt = self.add_info(repeat_txt, self.get_unique_id())
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            s.connect((self.target_ip, self.target_port))
            s.sendall(repeat_txt.encode())
            recv = s.recv(40960)

            try:
                status_code = recv[9:12].decode()
            except:
                status_code = '000'

            # 发包过快时判断出错,该部分判断关闭
            # 安恒waf拦截提示
            # if recv.find("因权限问题或行为非法".encode()) != -1:
            #     status_code = '600'
            # 长亭waf拦截提示
            # elif recv.find("可能对网站造成安全威胁".encode()) != -1:
            # elif recv.find(
            #         "s6DGZGcQ6wCRsrIgtOcl4RZ7Seuk3SWur9XG/wPUQSu/Dx8bpQAAAABJRU5ErkJggg==\"><title".encode()) != -1:
            #     status_code = '700'

        except socket.timeout as msg:
            # 如果超时,状态码111
            color_print("[*] 发送{}请求时超时{}".format(id, msg), 'red')
            status_code = '111'
            # print(repeat_txt)
        except ConnectionResetError as msg:
            # 如果端口满了被拒绝状态码110,后续会多次重试
            color_print("[*] 发送{}时连接出错{}".format(id, msg), 'red')
            status_code = '110'
        s.close()

        return status_code

    def pre_fix_pkg(self, data):
        if data[-3:] == "\r\n\r":
            data = data + "\n"
        return data

    def __senddata(self, id):
        repeat_txt = self.package[id] if self.fromsql else unquote(unescape(self.package[id]))
        # repeat_txt = unescape(self.package[id])

        # 修离谱的包格式错误
        repeat_txt = self.pre_fix_pkg(repeat_txt)

        # 修Content-Length
        repeat_txt = self.fix_package(repeat_txt)

        # 指定参数时替换Host
        if self.host:
            repeat_txt = re.sub(self.rep_host, self.host, repeat_txt)

        try:
            state_code = self.socket_repeat(id, repeat_txt)

            # 对ConnectionResetError处理,sleep一会再连吧..
            if state_code == '110':
                for _ in range(self.max_retry):
                    time.sleep(2)
                    state_code = self.socket_repeat(id, repeat_txt)
                    if state_code != '110':
                        color_print('[*] {}请求 重发后已正常'.format(id), 'green')
                        break

            # 尝试修复,并再次重发,若此时成功,如状态码不需要记录,则记为112
            if state_code == '111':
                fixed_package = self.fix_package(repeat_txt)
                state_code = self.socket_repeat(id, fixed_package)
                if state_code != '111':
                    color_print('[*] {}请求 修复后已正常'.format(id), 'green')
                    # state_code = '112'

            # 对需要记录的包进行记录
            if state_code in self.collection_code:
                self.response_code_package.setdefault(state_code, []).append(repeat_txt)

            # 对所有状态码数量进行记录
            self.response_code_num[state_code] = self.response_code_num.setdefault(state_code, 0) + 1

        except Exception as e:
            color_print('[*] 发送{}请求时出错{}'.format(id, e), "red")

    def save_package_to_file(self, start_order):
        '''
        :param start_order: 本次发包的起始编号,最后体现到发包汇总文件名
        :return:
        '''
        for code in self.collection_code:
            li = self.response_code_package.setdefault(code, [])
            if len(li) == 0: continue
            # 先进行url编码
            # li = [quote(l) for l in li]
            li = [l for l in li]
            writetxt = json.dumps(li, indent=4)
            file_name = self.code_event.setdefault(code, code)
            with open(os.path.join(self.savepath, "{}_{}.txt".format(file_name, start_order)), "w")as file:
                file.write(writetxt)

        # 每一波发完都清空结果
        self.response_code_package = {}

    def only_save_mode(self, output, start, end):
        self.savepath = output
        if not start == end == 0:
            if not (start <= end):
                color_print('[*] 起始/结束序号 参数有误', "redbold")
                return
            color_print("[*] 将记录序号从{}(包含) - {}(不包含) 的数据包 ,共计{}个".format(start, end, end - start), "blue")
        else:
            color_print("[*] 请正确配置记录包的起始和最终序号", "redbold")
            return
        self.collection_code = ["900"]
        self.response_code_package["900"] = self.package[start:end]
        self.save_package_to_file(start)

    def save_package_to_sql(self):
        insert_conn = mdb.connect(
            host=self.__cfg.get('SQL', 'host'),
            user=self.__cfg.get('SQL', 'user'),
            passwd=self.__cfg.get('SQL', 'pass'),
            db=self.__cfg.get('SQL', 'insert_database'),
            port=self.__cfg.getint('SQL', 'port'),
            charset='utf8'
        )

    def start_to_fuzz(self, output, start=0, end=0):
        self.total = len(self.package)
        color_print('[*] 共加载{}个样本.'.format(self.total), "blue")
        self.start_time = time.time()

        if not start == end == 0:
            if not (start <= end <= self.total):
                color_print('[*] 起始/结束序号 参数有误', "redbold")
                exit()
            self.start = start
            self.end = end
            self.total = end - start
            color_print("[*] 本次发包从{} - {} ,共计{}个".format(start, end, self.total), "blue")
        else:
            self.start = 0
            self.end = self.total

        # 每一次线程池发送一波数据包,发完后保存到文件,等同步,再继续发
        for packages_num in range(self.start, self.end)[::self.every_saved_packages]:
            color_print(
                "[*] 已检测 {} / {} , 进度 {:.2f} , 用时 {:.2f} s".format(packages_num - self.start, self.total,
                                                                   (packages_num - self.start) / 1.0 / self.total * 100,
                                                                   time.time() - self.start_time),
                "blue")
            pkgnum = min(packages_num + self.every_saved_packages, self.end)
            with ThreadPool(self.max_thread) as pool:
                pool.map(self.__senddata,
                         list(self.package.keys())[
                         packages_num:pkgnum])
                pool.close()
                pool.join()

            # 结果存储
            self.savepath = output
            if self.savepath != None:
                self.save_package_to_file(packages_num)

            # 输出当前状态
            self.print_status(pkgnum - self.start)

    # 修正中英文混合时format显示不齐
    def __calc_blank_len(self, total_len, string):
        for c in string:
            if ord(c) > 256:
                total_len -= 1
        return total_len

    def print_status(self, current_total):
        # 对记录到文件的状态码汇总输出
        rst_code_list = list(self.response_code_num.keys())
        rst_code_list.sort()
        for code in rst_code_list:
            check_out = self.response_code_num.setdefault(code, 0)
            if check_out > 0:
                event = self.code_event.setdefault(code, code)
                color_print(
                    "[*] 检测到{:>{lennum}}样本{:6}个,当前检测总样本{:10}个,占比{:.2f}% {}"
                        .format(event, check_out, current_total,
                                check_out / 1.0 / current_total * 100,
                                "已记录到文件" if code in self.collection_code and self.savepath != None else "",
                                lennum=self.__calc_blank_len(30, event)),
                    'yellow')

    def __del__(self):
        pass
