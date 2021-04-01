from abc import ABCMeta, abstractclassmethod


class StockInterface(metaclass=ABCMeta):
    # 抽象方法

    @classmethod
    def getBaseUrl(self): pass

    @classmethod
    def formatResultData(self, result): pass

    def getTagTitle(self):
        return "%-10s %-10s %-8s %-8s %-8s %-8s %-8s" % ("股票名称", "当前价格", "开盘价格", "昨收价格", "今最高价", "今最低价", "时间")
