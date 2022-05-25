import random
from module import common
from urllib.parse import unquote, quote


class nsfocus_xss:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def generate_payload(self, amount):

        xss_templates = '''
        <img src="livescript:document.vulnerable=true;">
        '''
        xss_templates = xss_templates.strip().split("\n")
        xss_templates = [i.strip() for i in xss_templates]
        for _ in range(amount):
            xss_template = random.choice(xss_templates)
            xss_template = self.common.replace(xss_template, 'NUM', 5)
            xss_template = self.common.replace(xss_template, 'STR', 5)
            xss_template = "{}={}".format(unquote(self.common.get_random_parame()[0]), quote(xss_template))
            self.payloads.append(xss_template)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="body_parame") for i in range(amount)]
        return packages
