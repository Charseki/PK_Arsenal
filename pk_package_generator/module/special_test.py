from .utils import color_print


class special_test:
    common = None
    payloads = []

    header_abort = ["info", "X-Devtools-Emulate-Network-Conditions-Client-Id"]
    parame_abort = []

    def generate_payload_parame(self, amount):
        for key in self.common.paramenames.keys():
            if key in self.header_abort: continue
            for value in self.common.paramenames[key]:
                txt_in_url_template = "{}={}".format(key, value)
                self.payloads.append(txt_in_url_template)

    def generate_payload_header(self, amount):
        for key in self.common.headers.keys():
            if key in self.header_abort: continue
            for value in self.common.headers[key]:
                header_template = "{}: {}".format(key, value)
                self.payloads.append(header_template)

    def generate_packages(self, options: list = None):
        packages = []

        # parame 逐个测试
        if "parame" in options:
            self.payloads = []
            amount = 0
            for i in self.common.paramenames.keys():
                if i in self.parame_abort:continue
                amount += len(self.common.paramenames[i])
            print("Parame: {}".format(amount))
            self.generate_payload_parame(amount)
            packages += [self.common.generate(self.payloads[i],
                                              method="POST",
                                              payload_location="body_parame",
                                              url="/notfound.jsp",
                                              header=[],
                                              body=[]) for i in range(amount)]
        # header逐个测试
        if "header" in options:
            self.payloads = []
            amount = 0
            for i in self.common.headers.keys():
                if i in self.header_abort: continue
                amount += len(self.common.headers[i])
            print("Header: {}".format(amount))
            self.generate_payload_header(amount)
            packages += [self.common.generate(self.payloads[i],
                                              method="GET",
                                              payload_location="other_head",
                                              url="/notfound.jsp",
                                              header=[],
                                              body=[]) for i in range(amount)]

        return packages

    def __init__(self, common=None):
        if (common != None):
            self.common = common
        else:
            color_print("注意: common未初始化", "redbold")
            self.common = common.common("./config.ini")
