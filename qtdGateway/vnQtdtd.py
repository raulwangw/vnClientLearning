#-*- coding:UTF-8 -*-
import sys
from inspect import getmembers


print(sys.version)

from vnqtdtd import TdApi





class sC(TdApi):
    connected = False
    def __init__(self):
        super(sC, self).__init__()
        self.createFtdcTdApi("12a")
        d2 = {}
        d2["type"] = 1
        d2["address"]="61.152.107.173"
        d2["port"]=7707
        self.registerFront(d2)
        self.init()
    
    def tdApi(self,t,d):
        self.reqApi(t,d)
    
    def onConnected(self,error):
        self.connected = True
        print(error)
        
    
    def onClosed(self,error):
        self.connected = False
        print(error)
            
            
    def onLogon(self,error,sid,last):
        print("onRspError")
        print(error)
        
    def onLogoff(self,data,error):
        print(data)
        print(error)

    def onQueryData(self,data,error):
        print(data)
        print(error)
        
    def OnSendOrder(self,data,error):
        print(data)
        print(error)
        
    def OnCancelOrder(self,data,error):
        print(data)
        print(error)
        
    def OnGetQuote(self,data,error):
        print(data)
        print(error)
        
    def OnRepay(self,data,error):
        print(data)
        print(error)
        
    def OnQueryHistoryData(self,data,error):
        print(data)
        print(error)
        
    def OnQueryDatas(self,data,error):
        print(data)
        print(error)
        
    def OnSendOrders(self,data,error):
        print(data)
        print(error)
        
    def OnCancelOrders(self,data,error):
        print(data)
        print(error)
        
    def OnGetQuotes(self,data,error):
        print(data)
        print(error)
        
    def OnQueryMultiAccountsDatas(self,data,error):
        print(data)
        print(error)
        
    def OnSendMultiAccountsOrders(self,data,error):
        print(data)
        print(error)
        
    def OnCancelMultiAccountsOrders(self,data,error):
        print(data)
        print(error)
        
    def OnGetMultiAccountsQuotes(self,data,error):
        print(data)
        print(error)
    
    def __del__(self):
        self.deInit()
        print("_delete_")
        

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
        1:OnConnected\n\
        2:OnClosed\n\
        3:OnLogon\n\
        4:OnLogoff\n\
        5:OnQueryData\n\
        6:OnSendOrder\n\
        7:OnCancelOrder\n\
        8:OnGetQuote\n\
        9:OnRepay\n\
        10:OnQueryHistoryData\n\
        11:OnQueryDatas\n\
        12:OnSendOrders\n\
        13:OnCancelOrders\n\
        14:OnGetQuotes\n\
        15:OnQueryMultiAccountsDatas\n\
        16:OnSendMultiAccountsOrders\n\
        17:OnCancelMultiAccountsOrders\n\
        18:OnGetMultiAccountsQuotes\n\
        Please Enter Number:")
        if v == '0':
            s.reqLogoff(dict)
            import time
            time.sleep(1)
            break
        if v == "1":
            print("onFrontConnected")
        if v == "2":
            print("onFrontDisconnected")
        if v == "3":
            s.reqLogon(dict)
        if v == "4":
            s.reqLogoff(dict)
        if v == "5":
            s.reqQueryData(dict)
        if v == "6":
            s.reqSendOrder(dict)
        if v == "7":
            s.reqCancelOrder(dict)
        if v == "8":
            s.reqGetQuote(dict)
        if v == "9":
            s.reqRepay(dict)
        if v == "10":
            s.reqQueryHistoryData(dict)
        if v == "11":
            s.reqQueryDatas(dict)
        if v == "12":
            s.reqSendOrders(dict)
        if v == "13":
            s.reqCancelOrders(dict)
        if v == "14":
            s.reqGetQuotes(dict)
        if v == "15":
            s.reqQueryMultiAccountsDatas(dict)
        if v == "16":
            s.reqSendMultiAccountsOrders(dict)
        if v == "17":
            s.reqCancelMultiAccountsOrders(dict)
        if v == "18":
            s.reqGetMultiAccountsQuotes(dict)
        input("Press to Continue.")
