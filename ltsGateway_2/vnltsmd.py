from ctypes import *
from ctypes.wintypes import *
import win32api

class MdApi(object):
    def __init__(self):
        print("my MdApi __init__")
        self.strLog = ""
        self.clientid = 255
        self.er = None
        self.rtn = None
        
    def init(self):
        self.clientid = self.dll.TdxL2Hq_Connect(self.mdAddress,self.mdPort,self.rtn,self.er)
        try:
            logS="None"
            if self.clientid == 0:
                logS=str(self.rtn.raw)
            else:
                logS=str(self.er.raw)
            if self.clientid == 0:
                self.onFrontConnected()
            else:
                win32api.FreeLibrary(self.dll._handle)
            print("logonx : %s,%s,%s"%(logS,self.rtn.raw,self.er.raw))
        except Exception,self.er:
            print(self.er)
        finally:
            print(self.clientid)

    def onFrontConnected(self):
        pass

    def registerFront(self,mdAddress,mdPort):
        print("register ok")
        self.dll = WinDLL("ltsGateway/ltsmd.dll")
        self.er = create_string_buffer("", 256)
        self.rtn = create_string_buffer("", 256)
        self.mdAddress = mdAddress
        self.mdPort = mdPort
    
    def subscribeMarketData(self,req):
        pass
        
    def reqUserLogin(self,req,reqID):
        pass
    
    def createCusMdApi(self,path):
        print("createCusApi")
        pass
        
    def GetMinuteTimeData(self):
        pass
