#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------
# File Name          :json2bp.py
# Date               :2021/09/02 14:14:18
# Author             :Charseki.Chen
# Email              :chenshengkai@vip.qq.com
# Version            :V1.0.0
# Description        :json2BurpSuite
# --------------------------------------------------

import sys
from urllib.parse import unquote
import pyperclip

s = '"176": "GET /?post=insert%20dirs%20exec%20master.dbo.xp_blank>_dirtree%20c:\\%20 HTTP/1.1\nHost: 192.168.20.20\nCookie: __jsluid=212054dd61e138200873e40fdd803df7\nAccept-Encoding: gzip, deflate\nAccept: */*\nUser-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Win64; x64; Trident/7.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; Media Center PC 6.0; Tablet PC 2.0; Microsoft Outlook 16.0.8431; ms-office; MSOffice 16)\n\n\n",'
# s = input('请输入你的原始报文:')
try:
    s = s.strip()
    if s.find(':')!=-1:
        s = s.split(":")[1].strip().strip(",\"")
    else:
        s = s.strip().strip(",\"")
    s = unquote(s)
    breaklocal = s.find("********************")
    if (breaklocal != -1): s = s[:breaklocal]
    sys.stdout.write(s)
    pyperclip.copy(s)
except Exception as e:
    print(e)