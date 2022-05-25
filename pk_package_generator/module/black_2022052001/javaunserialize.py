# -*- coding: utf-8 -*-
from module import common
import os
import json
import random
from urllib.parse import quote, unquote



class javaunserialize:
    common = None
    payloads = []

    def generate_payload(self, amount):

        for _ in range(amount):
            nonepayload = "test=None"
            self.payloads.append(nonepayload)

    def generate_packages(self, amount):

        self.generate_payload(amount)
        payload = "/main/vminstance?%ac%ed%00%05%73%72%00%11%6a%61%76%61%2e%6c%61%6e%67%2e%49%6e%74%65%67%65%72%12%e2%a0%a4%f7%81%87%38%02%00%01%49%00%05%76%61%6c%75%65%78%72%00%10%6a%61%76%61%2e%6c%61%6e%67%0a%2e%4e%75%6d%62%65%72%86%ac%95%1d%0b%94%e0%8b%02%00%00%78%70%00%00%00%01"
        packages = [
            self.common.generate(self.payloads[i],
                                 method="POST",
                                 payload_location="body_parame",
                                 url=payload) for i in range(amount)
        ]

        return packages

    def __init__(self, common=None):
        if (common != None):
            self.common = common
