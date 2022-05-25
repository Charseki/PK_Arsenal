# -*- coding: utf-8 -*-
from module import common
import os
import json
import random
from urllib.parse import quote, unquote


class shell_xxx:
    common = None
    payloads = []

    def generate_payload(self, amount):
        list_template = ["password-reset-introduction.txt"]
        for _ in range(amount):
            # 5%几率固定名字
            if random.randint(0, 100) <= 5:
                tmpname = random.choice(list_template)
            else:
                filename = os.path.splitext(self.common.get_random_filename())[0]
                tmpname = '{}shell.{}'.format(filename,
                                              random.choice(['php{}'.format(random.randint(0, 10000)), 'jsp']))
                tmpname = "".join([c.lower() if random.randint(0, 1) == 0 else c.upper() for c in tmpname])
            self.payloads.append(tmpname)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="GET",
                                         payload_location="file_name") for i in range(amount)]

        return packages

    def __init__(self, common=None):
        if (common != None):
            self.common = common
