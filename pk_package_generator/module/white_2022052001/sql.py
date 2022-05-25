import random
from module import common
from urllib.parse import unquote, quote


class sql:
    common = None
    payloads = []

    def __init__(self, common=None):
        if (common != None):
            self.common = common

    def generate_payload(self, amount):
        names = ["Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia", "Evelyn", "Abigail",
                 "Liam", "Noah", "William", "James", "Logan", "Benjamin", "Mason", "Elijah", "Oliver", "Jacob"]
        adverbs = ["angrily", "badly", "bravely", "calmly", "carefully", "easily", "fast", "happily", "hurriedly",
                   "loud", "loudly", "quickly", "quietly", "rapidly", "slowly", "slightly", "suddenly"]
        sql_templates = '''
        student union select {} to {} and {} join into party into show
        '''
        for _ in range(amount):
            sql_template = sql_templates.strip().format(random.choice(names),
                                                        random.choice(adverbs),
                                                        random.choice(adverbs))
            sql_template = "{}={}".format(unquote(self.common.get_random_parame()[0]), quote(sql_template))

            self.payloads.append(sql_template)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="body_parame") for i in range(amount)]
        return packages
