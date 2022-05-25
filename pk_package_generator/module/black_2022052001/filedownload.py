# -*- coding: utf-8 -*-
from module import common
import os
import json
import random
from urllib.parse import quote,unquote

class filedownload:

    common = None
    payloads = []

    def generate_payload(self,amount):

        for _ in range(amount):
            tmpname = ['test3693.war','icesword.war','xshock-0.1.tar.gz']
            self.payloads.append(random.choice(tmpname))

    def generate_packages(self,amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="GET",
                                         payload_location="file_name") for i in range(amount)]

        return packages

    def __init__(self,common=None):
        if(common!=None):
            self.common=common
