import random
from module import common
from urllib.parse import unquote, quote


class spider:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def generate_payload(self, amount):
        spiders = ["Speedy Spider", "lwp-trivial", "FAST-WebCrawler", "NetResearchServer", "FAST Enterprise Crawler",
                   "htdig", "DataparkSearch", "TurnitinBot", "Scrubby", "Gaisbot", "FyberSpider", "polybot", "TheSuBot",
                   "webcollage", "boitho", "Zao Bot", "Baiduspider", "Gigabot", "Exabot", "Jyxobot", "cosmos",
                   "BlitzBOT", "Pompos", "Mediapartners-Google", "YahooSeeker", "ia_archiver", "SpankBot", "NutchCVS",
                   "UdmSearch", "teoma_admin", "teoma_agent", "updated/0.1beta=Updated.com"]

        for _ in range(amount):
            header_template = "{}: {}".format("User-Agent", random.choice(spiders))
            self.payloads.append(header_template)

    def generate_packages(self, amount):
        # 预处理,只要调用到该插件,素材包里就不会再出现该header
        self.common.headers.pop("User-Agent", None)
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="other_head") for i in range(amount)]
        return packages
