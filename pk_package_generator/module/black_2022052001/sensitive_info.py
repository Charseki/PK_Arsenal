# -*- coding: utf-8 -*-
from module import common
import os
import json
import random
from urllib.parse import quote,unquote

class sensitive_info:

    common = None
    payloads = []

    def generate_payload(self,amount):
        suf_fix = ["config","conf","key","mdb"]
        for _ in range(amount):
            filename = "{}.{}".format(os.path.splitext(self.common.get_random_filename())[0],random.choice(suf_fix))
            self.payloads.append(filename)

    def generate_packages(self,amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="GET",
                                         payload_location="file_name") for i in range(amount)]

        return packages

    def __init__(self,common=None):
        if(common!=None):
            self.common=common
