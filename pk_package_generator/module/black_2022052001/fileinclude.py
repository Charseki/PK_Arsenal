import random
from module import common
from urllib.parse import unquote, quote


class fileinclude:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def make_issue(self):
        return "/etc/issue"

    def make_proc(self):
        return "/proc/{}/cmdline".format(random.randint(1,65535))

    def generate_payload(self, amount):
        # payload_templates = ["/etc/issue","/proc/1/cmdline"]
        for _ in range(amount):
            payload = random.choice([self.make_issue,self.make_proc])()
            parame = "{}={}".format(self.common.get_random_parame()[0], payload)
            self.payloads.append(parame)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="body_parame") for i in range(amount)]
        return packages
