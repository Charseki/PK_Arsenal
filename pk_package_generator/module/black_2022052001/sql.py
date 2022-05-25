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
        keywords = ['handler', 'read', 'where', 'create', 'table', 'select', 'from','as']

        # 预增加
        #create table STR select STR from STR
        sql_templates = '''
        handler STR read STR = (STR,STR,STR) where NUM=NUM
        handler STR read STR = (STR,STR)
        create table STR select STR from STR
        '''


        sql_templates = sql_templates.strip().split("\n")
        sql_templates = [i.strip() for i in sql_templates]
        for _ in range(amount):
            sql_template = random.choice(sql_templates)
            sql_template = self.common.replace(sql_template, 'NUM', 5)
            sql_template = self.common.change_case(sql_template, keywords)
            sql_template = self.common.replace(sql_template, 'STR', 10,3)
            sql_template = "{}={}".format(unquote(self.common.get_random_parame()[0]), quote(sql_template))
            self.payloads.append(sql_template)

    def generate_packages(self, amount):
        self.generate_payload(amount)
        packages = [self.common.generate(self.payloads[i],
                                         method="POST",
                                         payload_location="body_parame") for i in range(amount)]
        return packages
