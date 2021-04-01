import datetime
import random
import threading
import time

import requests


class Fund:
    def __init__(self, stockSource, ua):
        self.headers = {
            'authority': 'ec.snssdk.com',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                          "/86.0.4240.198 Safari/537.36 Edg/86.0.622.69 ",
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9,application/json',
            'content-type': 'application/json; charset=utf-8',

        }
        with open("../config/fund.txt", "r+", encoding="utf-8") as f:
            self.stockList = f.read().split("\n")
        self.stockSource = stockSource
        self.baseUrl = self.getBaseUrl()
        self.userAgents = ua

    def run(self):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        msgtag = "%-10s %-10s %-8s %-8s %-8s %-8s %-8s" % ("基金名称", "当前价格", "昨收价格", "昨收价格", "今最高价", "今最低价", "时间")
        self.msg = ""
        for stock in self.stockList:
            response = self.getUrl(stock)
            # 获取请求状态码 200为正常
            if response.status_code == 200:
                # 获取相应内容
                content = response.content
                # print("json content:", content)
                # print("decode ", res)
                # json_data = json.loads(res)
                try:
                    self.formatResult(content)
                except Exception as e:
                    msg = "请求成功，解析异常：" + repr(e) + "  " + self.currentUrl + "\n"
                    # print(msg)
                    self.msg += msg
            else:
                msg = stock + ":请求失败：" + repr(response.reason) + "  " + self.currentUrl + "\n"
                # print(msg)
                self.msg += msg
        print(msgtag)
        print(self.msg)
        self.loop()

    def loop(self):
        minute = datetime.datetime.now().minute
        if minute % 10 == 9:
            self.refreshConfig()
        self.timer = threading.Timer(1, self.run)
        self.timer.start()

    def getUrl(self, stockId):
        headers = {'User-Agent': random.choice(self.userAgents)}
        self.headers.update(headers)
        self.currentUrl = self.baseUrl.format(stockId)
        # print("url-->" + self.currentUrl)
        return requests.get(url=self.currentUrl, headers=self.headers, timeout=2.0)

    def formatResult(self, json_data):
        if self.stockSource == "sina":
            self.formatSina(json_data)
        else:
            self.formatTianTian(json_data)

    def getBaseUrl(self):
        if self.stockSource == "sina":
            return "http://hq.sinajs.cn/list={}"
        else:
            return ""

    def formatTianTian(self):
        pass

    def formatSina(self, raw):
        # http://hq.sinajs.cn/list=f_320007
        # var hq_str_f_320007="诺安成长混合,1.532,1.977,1.526,2021-03-31,189.564";
        data = bytes.decode(raw, encoding="gbk")
        data.replace("\";", "")
        start = data.index("\"") + 1
        list = data[start:].split(",")
        msg = "%-10s %-10s %-10s %-10s %-10s %-10s %-10s  %s\n" % (
        list[0], list[3], list[1], list[2], list[4], list[5], list[31], self.currentUrl)
        self.msg += msg
        pass

    def refreshConfig(self):
        # print("refreshConfig")
        with open("../config/fund.txt", "r+", encoding="utf-8") as f:
            self.stockList = f.read().split("\n")
