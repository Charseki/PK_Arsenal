# -*- coding: utf-8 -*-
from module import common
import os
import json
import random
from urllib.parse import quote, unquote


class shell_inj_learning:
    common = None
    payloads = []

    def generate_payload(self, amount):
        rangechars = "".join([chr(i) for i in range(0, 128)])
        dropchars = ['\x01','!','#','$','(',')','<','>','=','{','}','&','\x7f',';','|','\x0a','"','\'','%']
        dropappend= ['[',']']
        for c in dropchars:
            rangechars=rangechars.replace(c,'')
        for _ in range(amount):
            length = random.randint(10, 20)
            pkg = [random.choice(rangechars) for __ in range(length)]
            # pkg = [chr(65) for __ in range(length)]
            locats = random.sample(range(length), 4)
            locats.sort()
            # char_list = ['=', '`', '>', '`']
            char_list = ['=', '`', random.choice(['>','<',';','|']), '`']
            # print(locats)
            for num, loc in enumerate(locats[::-1]):
                pkg.insert(loc, char_list[3 - num])
            url = ",".join(str(i) for i in locats)
            self.payloads.append((url, "".join(pkg)))

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i][1],
                                         method="POST",
                                         url="/?{}".format(self.payloads[i][0]),
                                         header=[],
                                         body=[],
                                         payload_location="body_parame") for i in range(amount)]

        return packages

    def __init__(self, common=None):
        if (common != None):
            self.common = common
