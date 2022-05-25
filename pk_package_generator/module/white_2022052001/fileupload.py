import random
from module import common
from urllib.parse import unquote, quote


class fileupload:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def generate_payload(self, amount):
        phpwebshell_template_ori = '''aaa'''

        for _ in range(amount):
            file_name = '{}\\'.format(self.common.get_random_filename().split('.')[0])
            phpwebshell_template = 'name="test";filename="{}";\r\n\r\n{}'.format(file_name, phpwebshell_template_ori)
            self.payloads.append(phpwebshell_template)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location='body_parame',
                                         encoding='multipart') for i in range(amount)]
        return packages
