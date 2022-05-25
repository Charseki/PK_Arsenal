import random
from module import common
from urllib.parse import unquote, quote


class cross_path:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common


    def generate_payload(self, amount):
        payload_templates = ["\\u002f\\u002e\\u002e\\x2fsvn"]
        for _ in range(amount):
            payload = random.choice(payload_templates)
            parame = "{}={}".format(self.common.get_random_parame()[0], payload)
            self.payloads.append(parame)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="body_parame") for i in range(amount)]
        return packages
