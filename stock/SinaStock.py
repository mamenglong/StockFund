from stock.StockInterface import StockInterface


class SinaStock(StockInterface):

    def getBaseUrl(self):
        return "http://hq.sinajs.cn/list={}"

    def formatResultData(self, result):
        ##http://hq.sinajs.cn/list=sh601006
        ##var hq_str_sh601006="大秦铁路,7.020,7.010,6.950,7.030,6.920,6.950,6.960,23243977,161796810.000,87850,6.950,403900,6.940,791299,6.930,595500,6.920,317500,6.910,244198,6.960,286414,6.970,354800,6.980,313380,6.990,311484,7.000,2021-04-01,15:00:00,00,";
        data = bytes.decode(result, encoding="gbk")
        data.replace("\";", "")
        start = data.index("\"") + 1
        list = data[start:].split(",")
        msg = "%-10s %-10s %-10s %-10s %-10s %-10s %-10s  %s\n" % (
            list[0], list[3], list[1], list[2], list[4], list[5], list[31], self.currentUrl)
        self.msg += msg
