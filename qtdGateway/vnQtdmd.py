#-*- coding:UTF-8 -*-
import sys
from vnqtdmd import MdApi







class sC(MdApi):
    connected = False
    def __init__(self):
        super(sC, self).__init__()
        self.createFtdcMdApi("12a")
        d2 = {}
        d2["type"] = 1
        d2["address"]="61.152.107.173"
        d2["port"]=7707
        self.registerFront(d2)
        d1 = {}
        d1["type"]=0
        d1["address"]="121.14.110.200"
        d1["port"]=443
        self.registerFront(d1)
        #self.reqQtdL2Hq_Connect()
    
    def mdApi(self,t,d):
        self.reqApi(t,d)
    
    def onFrontConnected(self,error):
        self.connected = True
        print(error)
        
    
    def onFrontDisconnected(self,error):
        self.connected = False
        print(error)
            
    
    def onHeartBeatWarning(self,n):
        print(sys._getframe().f_code.co_name)
        
    def onRspError(self,error,sid,last):
        print("onRspError")
        print(error)
        
    def onGetDetailTransactionData(self,data,error):
        print(data)
        print(error)

    def onGetDetailOrderData(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetSecurityQuotes10(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetBuySellQueue(self,data,error):
        print(data)
        print(error)
        
    def onQtdL2Hq_Connect(self,data,error):
        print(data)
        print(error)
        
    def onQtdL2Hq_Disconnect(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetSecurityCount(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetSecurityList(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetSecurityBars(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetIndexBars(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetMinuteTimeData(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetHistoryMinuteTimeData(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetTransactionData(self,data,error):
        print(data)
        print(error)
        
    def onGetQtd2Hq_GetHistoryTransactionData(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetSecurityQuotes(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetCompanyInfoCategory(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetCompanyInfoContent(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetXDXRInfo(self,data,error):
        print(data)
        print(error)
        
    def onGetQtdL2Hq_GetFinanceInfo(self,data,error):
        print(data)
        print(error)


if __name__ == "__main__":  
    s = sC()
    dict = {"errorid":1}
    dict["market"]=0
    dict["zqdm"]="002181"
    dict["start"]=0
    dict["count"]=4
    dict["marketL"]=[0,0,0,0]
    dict["zqdmL"]=["002181","002182","002183","002184"]
    dict["Category"]=3
    dict["date"]=20160302
    while False:
        v = input("type:")
        if v == '0':
            break;
        else:
            s.mdApi(int(v),dict)
        input("press to continue.")
    while True:
        v = input("Choose Function:\n\
        1:onFrontConnected\n\
        2:onFrontDisconnected\n\
        3:onHeartBeatWarning\n\
        4:onRspError\n\
        5:onGetDetailTransactionData\n\
        6:onGetDetailOrderData\n\
        7:onGetQtdL2Hq_GetSecurityQuotes10\n\
        8:onGetQtdL2Hq_GetBuySellQueue\n\
        9:onQtdL2Hq_Connect\n\
        10:onQtdL2Hq_Disconnect\n\
        11:onGetQtdL2Hq_GetSecurityCount\n\
        12:onGetQtdL2Hq_GetSecurityList\n\
        13:onGetQtdL2Hq_GetSecurityBars\n\
        14:onGetQtdL2Hq_GetIndexBars\n\
        15:onGetQtdL2Hq_GetMinuteTimeData\n\
        16:onGetQtdL2Hq_GetHistoryMinuteTimeData\n\
        17:onGetQtdL2Hq_GetTransactionData\n\
        18:onGetQtd2Hq_GetHistoryTransactionData\n\
        19:onGetQtdL2Hq_GetSecurityQuotes\n\
        20:onGetQtdL2Hq_GetCompanyInfoCategory\n\
        21:onGetQtdL2Hq_GetCompanyInfoContent\n\
        22:onGetQtdL2Hq_GetXDXRInfo\n\
        23:onGetQtdL2Hq_GetFinanceInfo\n\
        24:registerFront\n\
        Please Enter Number:")
        if v == '0':
            s.reqQtdL2Hq_Disconnect()
            import time
            time.sleep(1)
            break
        if v == "1":
            print("onFrontConnected")
        if v == "2":
            print("onFrontDisconnected")
        if v == "3":
            print("onHeartBeatWarning")
        if v == "4":
            print("onRspError")
        if v == "5":
            s.reqGetDetailTransactionData(dict)
        if v == "6":
            s.reqGetDetailOrderData(dict)
        if v == "7":
            s.reqGetQtdL2Hq_GetSecurityQuotes10(dict)
        if v == "8":
            s.reqGetQtdL2Hq_GetBuySellQueue(dict)
        if v == "9":
            s.reqQtdL2Hq_Connect()
        if v == "10":
            s.reqQtdL2Hq_Disconnect()
        if v == "11":
            s.reqGetQtdL2Hq_GetSecurityCount(dict)
        if v == "12":
            s.reqGetQtdL2Hq_GetSecurityList(dict)
        if v == "13":
            s.reqGetQtdL2Hq_GetSecurityBars(dict)
        if v == "14":
            s.reqGetQtdL2Hq_GetIndexBars(dict)
        if v == "15":
            s.reqGetQtdL2Hq_GetMinuteTimeData(dict)
        if v == "16":
            s.reqGetQtdL2Hq_GetHistoryMinuteTimeData(dict)
        if v == "17":
            s.reqGetQtdL2Hq_GetTransactionData(dict)
        if v == "18":
            s.reqGetQtd2Hq_GetHistoryTransactionData(dict)
        if v == "19":
            s.reqGetQtdL2Hq_GetSecurityQuotes(dict)
        if v == "20":
            s.reqGetQtdL2Hq_GetCompanyInfoCategory(dict)
        if v == "21":
            s.reqGetQtdL2Hq_GetCompanyInfoContent(dict)
        if v == "22":
            s.reqGetQtdL2Hq_GetXDXRInfo(dict)
        if v == "23":
            s.reqGetQtdL2Hq_GetFinanceInfo(dict)
        if v == "24":
            s.registerFront("61.152.107.173:7707")
        input("Press to Continue.")
