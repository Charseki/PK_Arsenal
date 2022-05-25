# -*- coding: utf-8 -*-
from module import common
import os
import json
import random
from urllib.parse import quote, unquote


class vul_error:
    common = None
    payloads = []

    def generate_payload(self, amount):

        for _ in range(amount):
            filename = "/plus/search.php?typeArr[']"
            self.payloads.append(filename)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="file_name",
                                         url = "/plus/search.php?typeArr['']") for i in range(amount)]
        return packages

    def __init__(self, common=None):
        if (common != None):
            self.common = common
