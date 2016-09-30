from ctypes import *
from ctypes.wintypes import *
import win32api
class TdApi(object):
    def __init__(self):
        self.clientid = 255
        self.dll = None
        
    def OpenTdx(self):
        self.dll.OpenTdx()
        
    def Logon(self,tdAddress,tdport,tdver,YybID,AccountNo,TradeAccount,JyPassword,TxPassword):
        try:
            print("td begin connection")
            self.clientid=self.dll.Logon(tdAddress,tdport,tdver,YybID,AccountNo,TradeAccount,JyPassword,TxPassword,self.er)
            return
            logS="None"
            if self.clientid == 0:
                logS="success"
            else:
                logS="fail"
                self.exitApi()
            print("logon : %s"%logS)
            print("%s,%d,%s,%d,%s,%s,%s,%s"%(tdAddress,tdport,tdver,YybID,AccountNo,TradeAccount,JyPassword,TxPassword))
            print(self.er.raw)
        except Exception,e:
            print(e)
        finally:
            print(self.clientid)
        
    def init(self):
        print("init")
        try:
            self.dll = WinDLL("ltsGateway/ltstd.dll")
        except Exception,e:
            print("error "+e)
        self.OpenTdx();
        self.er = create_string_buffer("", 256)
        self.rtn = create_string_buffer("", 256) 
        self.clientid = 255
        print(self.er.raw)

        self.onFrontConnected()
    
    def exitApi(self):
        win32api.FreeLibrary(self.dll._handle)
    
    def onFrontConnected(self):
        pass

    def registerFront(self,tdAddress,tdport):
        self.tdAddress = tdAddress
        self.tdport = int(tdport)
    
    def subscribeMarketData(self,req):
        pass
    
    def VtLogData(self):
        return self.strLog;
    
    def reqUserLogin(self,req,reqID):
        tdAddress = self.tdAddress
        tdport    = self.tdport
        tdver     = req["Tdver"]
        YybID     = req["YybID"]
        AccountNo = req["AccountNo"]
        TradeAccount = req["TradeAccount"]
        JyPassword = req["JyPassword"]
        TxPassword = req["TxPassword"]
        self.Logon(tdAddress,tdport,tdver,int(YybID),AccountNo,TradeAccount,JyPassword,TxPassword)
    
    def createCusTraderApi(self,path):
        print("createCusTraderApi")
        pass
        
    def subscribePrivateTopic(self,num):
        pass
    def subscribePublicTopic(self,num):
        pass
