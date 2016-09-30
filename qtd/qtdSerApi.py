#coding = UTF-8
import threading
import time
from qtd.qtdListener import qtdListener
from eventType import *
from vtGateway import *
import copy
class qtdSerApi(object):
    def __init__(self):
        self.testKLThread = None
    
    def testForKLine(self):
        self.testKL = Test(10) 
        self.testKL.start()
    
    def testMD(self):
        d = QtdMDData()
        qtdListener.notify(EVENT_MD, d)
        c = copy.deepcopy(d)
        c.qtdMarketID = "12"
        c.stockid = "334"
        qtdListener.notify(EVENT_MD, c)

    def activeStockSelectionStratistic(self,sname):
        if sname == "name1":
            data = QtdSSelStrastic()
            data.qtdStockSelectStratistic = "1"
            data.stockid = "xName1"
            data.uppercent = "5%"
            data.curprice = "16.1"
            qtdListener.notify(EVENT_SSELSTRATIS, data)
        if sname == "name2":
            data = QtdSSelStrastic()
            data.qtdStockSelectStratistic = "2"
            data.stockid = "xName2"
            data.uppercent = "-1%"
            data.curprice = "23"
            qtdListener.notify(EVENT_SSELSTRATIS, data)
 

class Test(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self._run_num = num

    def run(self):
        print("run test KL thread")
        global count, mutex
        mutex = threading.Lock()

        while self._run_num > 0:
            mutex.acquire()
            qtdListener.notify(EVENT_DAILY_KLINE, "122")
            mutex.release()
            
            time.sleep(1)
            self._run_num -= 1
