import json
from urllib.parse import quote, unquote
import string

res = []
global unsafe
unsafe = [
    'select', 'union', 'or ', 'or/*', 'or\'', 'or(', 'or+', 'and', 'xor', 'now(', 'order', 'delay', 'outfile', 'char',
    'when', 'sleep', 'where', 'order', 'if(', 'substr', 'mid(', 'distinct', 'concat(', 'concat (', 'like', 'regexp',
    '&&', '||',
    '../', '..\\', '..../', 'web-inf', 'passwd', 'echo', '/etc',
    '<?php', 'eval', 'exec', 'assert', 'system', 'preg_replace', 'assert', 'chr', 'array_map', 'fputs', 'fopen',
    'post', 'get', 'direct', 'php://', 'print(', 'md5(', 'function', 'file_put_contents',
    'bxss', 'iframe', 'onerror', 'onmouse', 'script',
    # java
    'classloader', 'java.lang', 'opensymphony',
    # win
    'netstat', 'ipconfig',
    '.ini', '.svn', '.git', '.log', '.sql', '.htpasswd', '.htaccess', '.bak', '.inc', '.mdb', '.dat', '.pwd',
    '.vb', '.idq', '.bat', '.asa', '.csr', '.cmd', '.htr', '.htw', '.DBF', '.ida', '.idc', '.ini', '.sys', '.db',
    '.cer', '.key', '.old', '.CDX', '.cs', '.log', '.Asa', '.dbf', '.xsd', '.cfg', '.lnk', '.git', '.sh_history',
    '.bashrc', '.conf', '.backup', 'wp-config.php', '${', 'index/\\think',
    '\r\n', '\x00', '\x0a', '\x0d',
    'shellshock', '_memberaccess', 'bytes=', '__construct', '/proc',
    # 新规则远程文件包含
    'http:', 'ftp:', 'https:', 'file:', 'gopher:', 'php:',
    'QGluaV9z', 'aW5pX3Nl', 'PD9waHAg',
    '.nsr',
    # 其他
    'ZWNobygiamlubGFpbGUiKTtkaWUoKTs=', './index.php', '_','expr','response.write'
]
unsafe = [i.lower() for i in unsafe]

global notheadchar
notheadchar = ['/', '\\', '$', '@', '\x0d', '\x0a']


def issafe(i):
    if i == '': return False
    global unsafe
    tmp = i.lower()
    for i in unsafe:
        if tmp.find(i) != -1:
            return False
    return True


def nothead(i):
    global notheadchar
    tmp = i.lower()
    for i in notheadchar:
        if tmp.find(i) != -1:
            return True
    return False


def urldecode(i):
    leni = len(i)
    while True:
        i = unquote(i)
        if leni == len(i): break
        leni = len(i)
    return i


def clean(f, head=False):
    res = {}
    with open(f.format(""), 'rb') as file:
        s = file.read()
        jsdata = json.loads(s)

        for k in jsdata.keys():
            tmpk = urldecode(k)
            if head and len(tmpk) > 20: continue
            if (not issafe(tmpk)) or nothead(tmpk): continue
            for num, v in enumerate(jsdata[k]):
                if (not head) and num >= 50: break
                if head and len(v) > 200: continue
                tmpv = urldecode(v)
                if issafe(tmpv):
                    res.setdefault(quote(quote(tmpk)), []).append(quote(tmpv) if head else quote(quote(tmpv)))
    all = 0
    for k, v in res.items(): all += len(v)
    lenmap = [(len(v), k) for k, v in res.items()]
    lenmap.sort(reverse=True)
    print(lenmap)
    print(len(res))
    print(all)
    with open(f.format('2'), 'w') as file:
        file.write(json.dumps(res, indent=4))

global unsafe_get
unsafe_get=['<html',# 我们waf 400 http响应分割
            ]

def notgetchar(content: str):
    for c in content:
        if c not in string.printable: return True
    for i in unsafe_get:
        if content.find(i)!=-1:
            return True
    return False


def getparame(f):
    res = {}
    with open(f.format("2"), 'rb') as file:
        s = file.read()
        jsdata = json.loads(s)
        for k in jsdata.keys():
            tmpk = urldecode(k)
            if len(tmpk) > 20 :continue
            if notgetchar(tmpk): continue
            for v in jsdata[k]:
                tmpv = urldecode(v)
                if notgetchar(tmpv): continue
                res.setdefault(quote(quote(tmpk)), []).append(quote(quote(tmpv)))
    all = 0
    for k, v in res.items(): all += len(v)
    lenmap = [(len(v), k) for k, v in res.items()]
    lenmap.sort(reverse=True)
    print(lenmap)
    print(len(res))
    print(all)
    with open(f.format('_get'), 'w') as file:
        file.write(json.dumps(res, indent=4))


clean('./source/parame_value{}.txt')
clean('./source/headers{}.txt', True)
getparame('./source/parame_value{}.txt')
