import random
from module import common
from urllib.parse import unquote, quote


class ssrf:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def make_rmi(self):
        tmp  = "rmi://{}/{}".format(self.common.get_random_host(),self.common.get_random_filename())
        return tmp

    def make_glob(self):
        tmp  = "glob://{}/{}".format(self.common.get_random_path(),self.common.get_random_filename().split(".")[0]+"txt")
        return tmp

    def generate_payload(self, amount):
        # payload_templates = ["rmi://127.0.0.1:9999/shownews","glob://ext/spl/examples/*.php"]
        for _ in range(amount):
            payload = random.choice([self.make_rmi,self.make_glob])()
            parame = "{}={}".format(self.common.get_random_parame()[0], payload)
            self.payloads.append(parame)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="body_parame") for i in range(amount)]
        return packages
