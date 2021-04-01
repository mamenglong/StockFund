import datetime
import random
import threading
import time

import requests

from stock.SinaStock import SinaStock
from stock.StockInterface import StockInterface


class Stock(StockInterface):
    def __init__(self, stockSource, ua):
        self.headers = {
            'authority': 'ec.snssdk.com',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                          "/86.0.4240.198 Safari/537.36 Edg/86.0.622.69 ",
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9,application/json',
            'content-type': 'application/json; charset=utf-8',

        }
        with open("../config/stock.txt", "r+", encoding="utf-8") as f:
            self.stockList = f.read().split("\n")
        self.stockSource = stockSource
        self.stockImpl = self.getStockImpl()
        self.userAgents = ua

    def run(self):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.stockImpl.msg = ""
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
                    self.formatResultData(content)
                except Exception as e:
                    msg = "请求成功，解析异常：" + repr(e) + "  " + self.stockImpl.currentUrl + "\n"
                    # print(msg)
                    self.stockImpl.msg += msg
            else:
                msg = stock + ":请求失败：" + repr(response.reason) + "  " + self.stockImpl.currentUrl + "\n"
                # print(msg)
                self.stockImpl.msg += msg
        print(self.getTagTitle())
        print(self.stockImpl.msg)
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
        self.stockImpl.currentUrl = self.getBaseUrl().format(stockId)
        return requests.get(url=self.stockImpl.currentUrl, headers=self.headers, timeout=2.0)

    def formatResultData(self, result):
        self.stockImpl.formatResultData(result)

    def getBaseUrl(self):
        return self.stockImpl.getBaseUrl()

    def refreshConfig(self):
        # print("refreshConfig")
        with open("../config/stock.txt", "r+", encoding="utf-8") as f:
            self.stockList = f.read().split("\n")

    def getStockImpl(self):
        if self.stockSource == "sina":
            return SinaStock()
        else:
            return ""
