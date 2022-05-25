import random
from module import common
from urllib.parse import unquote, quote


class scaner:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def generate_payload(self, amount):
        scanner = ["acunetix", "mozilla 1.0, sparc, solaris", "lwp::simple", "clshttp", "nsauditor", "webbench", "perl",
                   "htmlparser", "apachebench", "webbench", "useragent", "auto spider"]


        for _ in range(amount):
            header_template = "{}: {}".format("User-Agent", random.choice(scanner))
            self.payloads.append(header_template)


    def generate_packages(self, amount):
        # 预处理,只要调用到该插件,素材包里就不会再出现该header
        self.common.headers.pop("User-Agent", None)
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="other_head") for i in range(amount)]
        return packages
