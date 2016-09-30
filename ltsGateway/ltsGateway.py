# encoding: UTF-8

'''
vn.lts鐨刧ateway鎺ュ叆
'''

import os
import json

from vnltsmd import MdApi
from vnltstd import TdApi
#from vnltsqry import QryApi
from ltsDataType import *
from vtGateway import *


# 浠ヤ笅涓轰竴浜沄T绫诲瀷鍜孡TS绫诲瀷鐨勬槧灏勫瓧鍏�
# 浠锋牸绫诲瀷鏄犲皠
priceTypeMap= {}
priceTypeMap[PRICETYPE_LIMITPRICE] = defineDict["SECURITY_FTDC_OPT_LimitPrice"]
priceTypeMap[PRICETYPE_MARKETPRICE] = defineDict["SECURITY_FTDC_OPT_AnyPrice"]
priceTypeMap[PRICETYPE_FAK] = defineDict["SECURITY_FTDC_OPT_BestPrice"]
priceTypeMap[PRICETYPE_FOK] = defineDict["SECURITY_FTDC_OPT_AllLimitPrice"]
priceTypeMapReverse = {v: k for k, v in priceTypeMap.items()} 

# 鏂瑰悜绫诲瀷鏄犲皠
directionMap = {}
directionMap[DIRECTION_LONG] = defineDict["SECURITY_FTDC_D_Buy"]
directionMap[DIRECTION_SHORT] = defineDict["SECURITY_FTDC_D_Sell"]
directionMapReverse = {v: k for k, v in directionMap.items()}

# 寮�骞崇被鍨嬫槧灏�
offsetMap = {}
offsetMap[OFFSET_OPEN] = defineDict["SECURITY_FTDC_OF_Open"]
offsetMap[OFFSET_CLOSE] = defineDict["SECURITY_FTDC_OF_Close"]
offsetMap[OFFSET_CLOSETODAY] = defineDict["SECURITY_FTDC_OF_CloseToday"]
offsetMap[OFFSET_CLOSEYESTERDAY] = defineDict["SECURITY_FTDC_OF_CloseYesterday"]
offsetMapReverse = {v:k for k,v in offsetMap.items()}

# 浜ゆ槗鎵�绫诲瀷鏄犲皠
exchangeMap = {}
exchangeMap[EXCHANGE_SSE] = 'SSE'
exchangeMap[EXCHANGE_SZSE] = 'SZE'
exchangeMap[EXCHANGE_HKEX] = 'HGE'
exchangeMapReverse = {v:k for k,v in exchangeMap.items()}

# 鎸佷粨绫诲瀷鏄犲皠
posiDirectionMap = {}
posiDirectionMap[DIRECTION_NET] = defineDict["SECURITY_FTDC_PD_Net"]
posiDirectionMap[DIRECTION_LONG] = defineDict["SECURITY_FTDC_PD_Long"]
posiDirectionMap[DIRECTION_SHORT] = defineDict["SECURITY_FTDC_PD_Short"]
posiDirectionMapReverse = {v:k for k,v in posiDirectionMap.items()}


########################################################################################
class LtsGateway(VtGateway):
    """Lts鎺ュ彛"""

    #----------------------------------------------------------------------
    def __init__(self, eventEngine, gatewayName='LTS'):
        """Constructor"""
        super(LtsGateway, self).__init__(eventEngine, gatewayName)
        
        self.mdApi = LtsMdApi(self)
        self.tdApi = LtsTdApi(self)
        #self.qryApi = LtsQryApi(self)
        
        self.mdConnected = False
        self.tdConnected = False
        self.qryConnected = False
        
        self.qryEnabled = False         # 鏄惁瑕佸惎鍔ㄥ惊鐜煡璇�
    
    #----------------------------------------------------------------------
    def connect(self):
        """杩炴帴"""
        # 杞藉叆json 鏂囦欢
        fileName = self.gatewayName + '_connect.json'
        fileName = os.getcwd() + '/ltsGateway/' + fileName
        
        try:
            f = file(fileName)
        except IOError:
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'璇诲彇杩炴帴閰嶇疆鍑洪敊锛岃妫�鏌�'
            self.onLog(log)
            return
        
        # 瑙ｆ瀽json鏂囦欢
        setting = json.load(f)
        try:
            userID = str(setting['userID'])
            mdPassword = str(setting['mdPassword'])
            tdPassword = str(setting['tdPassword'])
            brokerID = str(setting['brokerID'])
            tdAddress = str(setting['tdAddress'])
            mdAddress = str(setting['mdAddress'])
            qryAddress = str(setting['qryAddress'])
            productInfo = str(setting['productInfo'])
            authCode = str(setting['authCode'])
        except KeyError:
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'杩炴帴閰嶇疆缂哄皯瀛楁锛岃妫�鏌�'
            self.onLog(log)
            return            
              
        # 鍒涘缓琛屾儏鍜屼氦鏄撴帴鍙ｅ璞�
        self.mdApi.connect(userID, mdPassword, brokerID, mdAddress)
        self.tdApi.connect(userID, tdPassword, brokerID, tdAddress, productInfo, authCode)
        #self.qryApi.connect(userID, tdPassword, brokerID, qryAddress, productInfo, authCode)
        
        # 鍒濆鍖栧苟鍚姩鏌ヨ
        self.initQuery()
        self.startQuery()
    
    #----------------------------------------------------------------------
    def subscribe(self, subscribeReq):
        """璁㈤槄琛屾儏"""
        self.mdApi.subscribe(subscribeReq)
        
    #----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """鍙戝崟"""
        return self.tdApi.sendOrder(orderReq)
        
    #----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """鎾ゅ崟"""
        self.tdApi.cancelOrder(cancelOrderReq)
        
    #----------------------------------------------------------------------
    def qryAccount(self):
        """鏌ヨ璐︽埛璧勯噾"""
        #self.qryApi.qryAccount()
        pass
        
    #----------------------------------------------------------------------
    def qryPosition(self):
        """鏌ヨ鎸佷粨"""
        #self.qryApi.qryPosition()
        pass
        
    #----------------------------------------------------------------------
    def close(self):
        """鍏抽棴"""
        if self.mdConnected:
            self.mdApi.close()
        if self.tdConnected:
            self.tdApi.close()
        #if self.qryConnected:
        #    self.qryApi.close()        
        
    #----------------------------------------------------------------------
    def initQuery(self):
        """鍒濆鍖栬繛缁煡璇�"""
        if self.qryEnabled:
            # 闇�瑕佸惊鐜殑鏌ヨ鍑芥暟鍒楄〃
            self.qryFunctionList = [self.qryAccount, self.qryPosition]
            
            self.qryCount = 0           # 鏌ヨ瑙﹀彂鍊掕鏃�
            self.qryTrigger = 2         # 鏌ヨ瑙﹀彂鐐�
            self.qryNextFunction = 0    # 涓婃杩愯鐨勬煡璇㈠嚱鏁扮储寮�
            
            self.startQuery()        
    
    #----------------------------------------------------------------------
    def query(self, event):
        """娉ㄥ唽鍒颁簨浠跺鐞嗗紩鎿庝笂鐨勬煡璇㈠嚱鏁�"""
        self.qryCount += 1
        
        if self.qryCount > self.qryTrigger:
            # 娓呯┖鍊掕鏃�
            self.qryCount = 0
            
            # 鎵ц鏌ヨ鍑芥暟
            function = self.qryFunctionList[self.qryNextFunction]
            function()
            
            # 璁＄畻涓嬫鏌ヨ鍑芥暟鐨勭储寮曪紝濡傛灉瓒呰繃浜嗗垪琛ㄩ暱搴︼紝鍒欓噸鏂拌涓�0
            self.qryNextFunction += 1
            if self.qryNextFunction == len(self.qryFunctionList):
                self.qryNextFunction = 0
    
    #----------------------------------------------------------------------
    def startQuery(self):
        """鍚姩杩炵画鏌ヨ"""
        self.eventEngine.register(EVENT_TIMER, self.query)
    
    #----------------------------------------------------------------------
    def setQryEnabled(self, qryEnabled):
        """璁剧疆鏄惁瑕佸惎鍔ㄥ惊鐜煡璇�"""
        self.qryEnabled = qryEnabled    


########################################################################
class LtsMdApi(MdApi):
    """Lts琛屾儏API瀹炵幇"""

    #----------------------------------------------------------------------
    def __init__(self, gateway):
        """Constructor"""
        super(LtsMdApi, self).__init__()
        
        self.gateway = gateway                     #gateway瀵硅薄
        self.gatewayName = gateway.gatewayName     #gateway瀵硅薄鍚嶇О
        
        self.reqID = EMPTY_INT                  # 鎿嶄綔璇锋眰缂栧彿
        
        self.connectionStatus = False           # 杩炴帴鐘舵��
        self.loginStatus = False                # 鐧婚檰鐘舵��
        
        self.subscribedSymbols = set()
        
        self.userID = EMPTY_STRING          # 璐﹀彿
        self.password = EMPTY_STRING        # 瀵嗙爜
        self.brokerID = EMPTY_STRING        # 缁忕邯鍟嗕唬鐮�
        self.address = EMPTY_STRING         # 鏈嶅姟鍣ㄥ湴鍧�            
    
    #----------------------------------------------------------------------
    def onFrontConnected(self):
        """鏈嶅姟鍣ㄨ繛鎺�"""
        self.connectionStatus = True
        
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = u'琛屾儏鏈嶅姟鍣ㄨ繛鎺ユ垚鍔�'
        self.gateway.onLog(log)
        self.login()
        
    #----------------------------------------------------------------------
    def onFrontDisconnected(self,n):
        """鏈嶅姟鍣ㄦ柇寮�"""
        self.connectionStatus= False
        self.loginStatus = False
        self.gateway.mdConnected = False
        
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = u'琛屾儏鏈嶅姟鍣ㄨ繛鎺ユ柇寮�'
        self.gateway.onLog(log) 
        
    #----------------------------------------------------------------------
    def onHeartBeatWarning(self, n):
        """蹇冭烦鎶ヨ"""
        pass
    
    #----------------------------------------------------------------------
    def onRspError(self,error,n,last):
        """閿欒鍥炴姤"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------        
    def onRspUserLogin(self, data, error, n, last):
        """鐧婚檰鍥炴姤"""
        # 濡傛灉鐧诲綍鎴愬姛锛屾帹閫佹棩蹇椾俊鎭�
        if error['ErrorID'] == 0:
            self.loginStatus = True
            self.gateway.mdConnected = True
            
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'琛屾儏鏈嶅姟鍣ㄧ櫥褰曞畬鎴�'
            self.gateway.onLog(log)
            
            # 閲嶆柊璁㈤槄涔嬪墠璁㈤槄鐨勫悎绾�
            for subscribeReq in self.subscribedSymbols:
                self.subscribe(subscribeReq)
                
        # 鍚﹀垯锛屾帹閫侀敊璇俊鎭�
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)    
    
    #----------------------------------------------------------------------        
    def onRspUserLogout(self, data, error, n, last):
        """鐧诲嚭鍥炴姤"""
        # 濡傛灉鐧诲嚭鎴愬姛锛屾帹閫佹棩蹇椾俊鎭�
        if error['ErrorID'] == 0:
            self.loginStatus = False
            self.gateway.tdConnected = False
            
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'琛屾儏鏈嶅姟鍣ㄧ櫥鍑哄畬鎴�'
            self.gateway.onLog(log)
                
        # 鍚﹀垯锛屾帹閫侀敊璇俊鎭�
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)
            
    #----------------------------------------------------------------------  
    def onRspSubMarketData(self, data, error, n, last):
        """璁㈤槄鍚堢害鍥炴姤"""
        # 閫氬父涓嶅湪涔庤闃呴敊璇紝閫夋嫨蹇界暐
        pass
        
    #----------------------------------------------------------------------  
    def onRspUnSubMarketData(self, data, error, n, last):
        """閫�璁㈠悎绾﹀洖鎶�"""
        # 鍚屼笂
        pass  
        
    #----------------------------------------------------------------------  
    def onRtnDepthMarketData(self, data):
        """琛屾儏鎺ㄩ��"""
        tick = VtTickData()
        tick.gatewayName = self.gatewayName
        
        tick.symbol = data['InstrumentID']
        tick.exchange = exchangeMapReverse.get(data['ExchangeID'], u'鏈煡')
        tick.vtSymbol = '.'.join([tick.symbol, tick.exchange])
        
        tick.lastPrice = data['LastPrice']
        tick.volume = data['Volume']
        tick.openInterest = data['OpenInterest']
        tick.time = '.'.join([data['UpdateTime'], str(data['UpdateMillisec']/100)])
        tick.date = data['TradingDay']
        
        tick.openPrice = data['OpenPrice']
        tick.highPrice = data['HighestPrice']
        tick.lowPrice = data['LowestPrice']
        tick.preClosePrice = data['PreClosePrice']
        
        tick.upperLimit = data['UpperLimitPrice']
        tick.lowerLimit = data['LowerLimitPrice']        
        
        # LTS鏈�5妗ｈ鎯�
        tick.bidPrice1 = data['BidPrice1']
        tick.bidVolume1 = data['BidVolume1']
        tick.askPrice1 = data['AskPrice1']
        tick.askVolume1 = data['AskVolume1']
        
        tick.bidPrice2 = data['BidPrice2']
        tick.bidVolume2 = data['BidVolume2']
        tick.askPrice2 = data['AskPrice2']
        tick.askVolume2 = data['AskVolume2']  
        
        tick.bidPrice3 = data['BidPrice3']
        tick.bidVolume3 = data['BidVolume3']
        tick.askPrice3 = data['AskPrice3']
        tick.askVolume3 = data['AskVolume3']
        
        tick.bidPrice4 = data['BidPrice4']
        tick.bidVolume4 = data['BidVolume4']
        tick.askPrice4 = data['AskPrice4']
        tick.askVolume4 = data['AskVolume4']
        
        tick.bidPrice5 = data['BidPrice5']
        tick.bidVolume5 = data['BidVolume5']
        tick.askPrice5 = data['AskPrice5']
        tick.askVolume5 = data['AskVolume5']        
        
        self.gateway.onTick(tick)
        
    #----------------------------------------------------------------------
    def connect(self, userID, password, brokerID, address):
        """鍒濆鍖栬繛鎺�"""
        self.userID = userID                # 璐﹀彿
        self.password = password            # 瀵嗙爜
        self.brokerID = brokerID            # 缁忕邯鍟嗕唬鐮�
        self.address = address              # 鏈嶅姟鍣ㄥ湴鍧�
        
        # 濡傛灉灏氭湭寤虹珛鏈嶅姟鍣ㄨ繛鎺ワ紝鍒欒繘琛岃繛鎺�
        if not self.connectionStatus:
            # 鍒涘缓C++鐜涓殑API瀵硅薄锛岃繖閲屼紶鍏ョ殑鍙傛暟鏄渶瑕佺敤鏉ヤ繚瀛�.con鏂囦欢鐨勬枃浠跺す璺緞
            path = os.getcwd() + '/temp/' + self.gatewayName + '/'
            if not os.path.exists(path):
                os.makedirs(path)
            self.createFtdcMdApi(path)
            
            # 娉ㄥ唽鏈嶅姟鍣ㄥ湴鍧�
            self.registerFront(self.address)
            
            # 鍒濆鍖栬繛鎺ワ紝鎴愬姛浼氳皟鐢╫nFrontConnected
            self.init()
            
        # 鑻ュ凡缁忚繛鎺ヤ絾灏氭湭鐧诲綍锛屽垯杩涜鐧诲綍
        else:
            if not self.loginStatus:
                self.login()
        
    #----------------------------------------------------------------------
    def subscribe(self, subscribeReq):
        """璁㈤槄鍚堢害"""
        req = {}
        req['InstrumentID'] = str(subscribeReq.symbol)
        req['ExchangeID'] = exchangeMap.get(str(subscribeReq.exchange), '')
        
        # 杩欓噷鐨勮璁℃槸锛屽鏋滃皻鏈櫥褰曞氨璋冪敤浜嗚闃呮柟娉�
        # 鍒欏厛淇濆瓨璁㈤槄璇锋眰锛岀櫥褰曞畬鎴愬悗浼氳嚜鍔ㄨ闃�
        if self.loginStatus:
            self.subscribeMarketData(req)
        
        self.subscribedSymbols.add(subscribeReq)   
        
    #----------------------------------------------------------------------
    def login(self):
        """鐧诲綍"""
        # 濡傛灉濉叆浜嗙敤鎴峰悕瀵嗙爜绛夛紝鍒欑櫥褰�
        if self.userID and self.password and self.brokerID:
            req = {}
            req['UserID'] = self.userID
            req['Password'] = self.password
            req['BrokerID'] = self.brokerID
            self.reqID += 1
            self.reqUserLogin(req, self.reqID)    

    #----------------------------------------------------------------------
    def close(self):
        """鍏抽棴"""
        self.exit()        
        
        
########################################################################
class LtsTdApi(TdApi):
    """LTS浜ゆ槗API瀹炵幇"""
    
    #----------------------------------------------------------------------
    def __init__(self, gateway):
        """API瀵硅薄鐨勫垵濮嬪寲鍑芥暟"""
        super(LtsTdApi, self).__init__()
        
        self.gateway = gateway                  # gateway瀵硅薄
        self.gatewayName = gateway.gatewayName  # gateway瀵硅薄鍚嶇О
        
        self.reqID = EMPTY_INT              # 鎿嶄綔璇锋眰缂栧彿
        self.orderRef = EMPTY_INT           # 璁㈠崟缂栧彿
        
        self.connectionStatus = False       # 杩炴帴鐘舵��
        self.loginStatus = False            # 鐧诲綍鐘舵��
        
        self.userID = EMPTY_STRING          # 璐﹀彿
        self.password = EMPTY_STRING        # 瀵嗙爜
        self.brokerID = EMPTY_STRING        # 缁忕邯鍟嗕唬鐮�
        self.address = EMPTY_STRING         # 鏈嶅姟鍣ㄥ湴鍧�
        self.productInfo = EMPTY_STRING     # 绋嬪簭浜у搧鍚嶇О
        self.authCode = EMPTY_STRING        # 鎺堟潈鐮�
        self.randCode = EMPTY_STRING        # 闅忔満鐮�
        
        self.frontID = EMPTY_INT            # 鍓嶇疆鏈虹紪鍙�
        self.sessionID = EMPTY_INT          # 浼氳瘽缂栧彿
        
    #----------------------------------------------------------------------
    def onFrontConnected(self):
        """鏈嶅姟鍣ㄨ繛鎺�"""
        self.connectionStatus = True
        
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = u'浜ゆ槗鏈嶅姟鍣ㄨ繛鎺ユ垚鍔�'
        self.gateway.onLog(log)
        
        # 鍓嶇疆鏈鸿繛鎺ュ悗锛岃姹傞殢鏈虹爜
        self.reqID += 1
        self.reqFetchAuthRandCode({}, self.reqID)        
    
    #----------------------------------------------------------------------
    def onFrontDisconnected(self, n):
        """鏈嶅姟鍣ㄦ柇寮�"""
        self.connectionStatus = False
        self.loginStatus = False
        self.gateway.tdConnected = False
        
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = u'浜ゆ槗鏈嶅姟鍣ㄨ繛鎺ユ柇寮�'
        self.gateway.onLog(log)      
    
    #----------------------------------------------------------------------
    def onHeartBeatWarning(self, n):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def onRspUserLogin(self, data, error, n, last):
        """鐧婚檰鍥炴姤"""
        # 濡傛灉鐧诲綍鎴愬姛锛屾帹閫佹棩蹇椾俊鎭�
        if error['ErrorID'] == 0:
            self.frontID = str(data['FrontID'])
            self.sessionID = str(data['SessionID'])
            self.loginStatus = True
            self.gateway.mdConnected = True
            
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'浜ゆ槗鏈嶅姟鍣ㄧ櫥褰曞畬鎴�'
            self.gateway.onLog(log)            
                
        # 鍚﹀垯锛屾帹閫侀敊璇俊鎭�
        else:
            err = VtErrorData()
            err.gatewayName = self.gateway
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspUserLogout(self, data, error, n, last):
        """鐧诲嚭鍥炴姤"""
        # 濡傛灉鐧诲嚭鎴愬姛锛屾帹閫佹棩蹇椾俊鎭�
        if error['ErrorID'] == 0:
            self.loginStatus = False
            self.gateway.tdConnected = False
            
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'浜ゆ槗鏈嶅姟鍣ㄧ櫥鍑哄畬鎴�'
            self.gateway.onLog(log)
                
        # 鍚﹀垯锛屾帹閫侀敊璇俊鎭�
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspFetchAuthRandCode(self, data, error, n, last):
        """璇锋眰闅忔満璁よ瘉鐮�"""
        self.randCode = data['RandCode']
        self.login()
   
    #----------------------------------------------------------------------    
    def onRspUserPasswordUpdate(self, data, error, n, last):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def onRspTradingAccountPasswordUpdate(self, data, error, n, last):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def onRspOrderInsert(self, data, error, n, last):
        """鍙戝崟閿欒锛堟煖鍙帮級"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspOrderAction(self, data, error, n, last):
        """鎾ゅ崟閿欒锛堟煖鍙帮級"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspError(self, error, n, last):
        """閿欒鍥炴姤"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRtnOrder(self, data):
        """鎶ュ崟鍥炴姤"""       
        # 鏇存柊鏈�澶ф姤鍗曠紪鍙�
        newref = data['OrderRef']
        self.orderRef = max(self.orderRef, int(newref))
        
        # 鍒涘缓鎶ュ崟鏁版嵁瀵硅薄
        order = VtOrderData()
        order.gatewayName = self.gatewayName
        
        # 淇濆瓨浠ｇ爜鍜屾姤鍗曞彿
        order.symbol = data['InstrumentID']
        order.exchange = exchangeMapReverse.get(data['ExchangeID'], '')
        order.vtSymbol = '.'.join([order.symbol, order.exchange])
        
        order.orderID = data['OrderRef']
        
        # 鏂瑰悜
        if data['Direction'] == '0':
            order.direction = DIRECTION_LONG
        elif data['Direction'] == '1':
            order.direction = DIRECTION_SHORT
        else:
            order.direction = DIRECTION_UNKNOWN
            
        # 寮�骞�
        if data['CombOffsetFlag'] == '0':
            order.offset = OFFSET_OPEN
        elif data['CombOffsetFlag'] == '1':
            order.offset = OFFSET_CLOSE
        else:
            order.offset = OFFSET_UNKNOWN
            
        # 鐘舵��
        if data['OrderStatus'] == '0':
            order.status = STATUS_ALLTRADED
        elif data['OrderStatus'] == '1':
            order.status = STATUS_PARTTRADED
        elif data['OrderStatus'] == '3':
            order.status = STATUS_NOTTRADED
        elif data['OrderStatus'] == '5':
            order.status = STATUS_CANCELLED
        else:
            order.status = STATUS_UNKNOWN
            
        # 浠锋牸銆佹姤鍗曢噺绛夋暟鍊�
        order.price = float(data['LimitPrice'])
        order.totalVolume = data['VolumeTotalOriginal']
        order.tradedVolume = data['VolumeTraded']
        order.orderTime = data['InsertTime']
        order.cancelTime = data['CancelTime']
        order.frontID = data['FrontID']
        order.sessionID = data['SessionID']
        
        # CTP鐨勬姤鍗曞彿涓�鑷存�х淮鎶ら渶瑕佸熀浜巉rontID, sessionID, orderID涓変釜瀛楁
        order.vtOrderID = '.'.join([self.gatewayName, order.orderID])
        
        # 鎺ㄩ��
        self.gateway.onOrder(order)
    
    #----------------------------------------------------------------------
    def onRtnTrade(self, data):
        """鎴愪氦鍥炴姤"""
        # 鍒涘缓鎶ュ崟鏁版嵁瀵硅薄
        trade = VtTradeData()
        trade.gatewayName = self.gatewayName
        
        # 淇濆瓨浠ｇ爜鍜屾姤鍗曞彿
        trade.symbol = data['InstrumentID']
        trade.exchange = exchangeMapReverse.get(data['ExchangeID'], '')
        trade.vtSymbol = '.'.join([trade.symbol, trade.exchange])
        
        trade.tradeID = data['TradeID']
        trade.vtTradeID = '.'.join([self.gatewayName, trade.tradeID])
        
        trade.orderID = data['OrderRef']
        trade.vtOrderID = '.'.join([self.gatewayName, trade.orderID])   
        
        # 鏂瑰悜
        trade.direction = directionMapReverse.get(data['Direction'], '')
            
        # 寮�骞�
        trade.offset = offsetMapReverse.get(data['OffsetFlag'], '')
            
        # 浠锋牸銆佹姤鍗曢噺绛夋暟鍊�
        trade.price = float(data['Price'])
        trade.volume = data['Volume']
        trade.tradeTime = data['TradeTime']
        
        # 鎺ㄩ��
        self.gateway.onTrade(trade)
    
    #----------------------------------------------------------------------
    def onErrRtnOrderInsert(self, data, error):
        """鍙戝崟閿欒鍥炴姤锛堜氦鏄撴墍锛�"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onErrRtnOrderAction(self, data, error):
        """鎾ゅ崟閿欒鍥炴姤锛堜氦鏄撴墍锛�"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspFundOutByLiber(self, data, error, n, last):
        """LTS鍙戣捣鍑洪噾搴旂瓟"""
        pass   
 
    #----------------------------------------------------------------------    
    def onRtnFundOutByLiber(self, data):
        """LTS鍙戣捣鍑洪噾閫氱煡"""
        pass        
    
    #----------------------------------------------------------------------
    def onErrRtnFundOutByLiber(self, data, error):
        """LTS鍙戣捣鍑洪噾閿欒鍥炴姤"""
        pass
    
    #----------------------------------------------------------------------
    def onRtnFundInByBank(self, data):
        """閾惰鍙戣捣鍏ラ噾閫氱煡"""
        pass

    #----------------------------------------------------------------------
    def onRspFundInterTransfer(self, data, error, n, last):
        """璧勯噾鍐呰浆搴旂瓟"""
        pass
    
    #----------------------------------------------------------------------
    def onRtnFundInterTransferSerial(self, data):
        """璧勯噾鍐呰浆娴佹按閫氱煡"""
        pass
    
    #----------------------------------------------------------------------
    def onErrRtnFundInterTransfer(self, data, error):
        """璧勯噾鍐呰浆閿欒鍥炴姤"""
        pass  
         
    #----------------------------------------------------------------------
    def connect(self, userID, password, brokerID, address, productInfo, authCode):
        """鍒濆鍖栬繛鎺�"""
        self.userID = userID                # 璐﹀彿
        self.password = password            # 瀵嗙爜
        self.brokerID = brokerID            # 缁忕邯鍟嗕唬鐮�
        self.address = address              # 鏈嶅姟鍣ㄥ湴鍧�
        self.productInfo = productInfo
        self.authCode = authCode
        
        # 濡傛灉灏氭湭寤虹珛鏈嶅姟鍣ㄨ繛鎺ワ紝鍒欒繘琛岃繛鎺�
        if not self.connectionStatus:
            # 鍒涘缓C++鐜涓殑API瀵硅薄锛岃繖閲屼紶鍏ョ殑鍙傛暟鏄渶瑕佺敤鏉ヤ繚瀛�.con鏂囦欢鐨勬枃浠跺す璺緞
            path = os.getcwd() + '/temp/' + self.gatewayName + '/'
            if not os.path.exists(path):
                os.makedirs(path)
            self.createFtdcTraderApi(path)
            
            # 璁剧疆鏁版嵁鍚屾妯″紡涓烘帹閫佷粠浠婃棩寮�濮嬫墍鏈夋暟鎹�
            self.subscribePrivateTopic(0)
            self.subscribePublicTopic(0)
            
            # 娉ㄥ唽鏈嶅姟鍣ㄥ湴鍧�
            self.registerFront(self.address)
            
            # 鍒濆鍖栬繛鎺ワ紝鎴愬姛浼氳皟鐢╫nFrontConnected
            self.init()
            
        # 鑻ュ凡缁忚繛鎺ヤ絾灏氭湭鐧诲綍锛屽垯杩涜鐧诲綍
        else:
            if not self.loginStatus:
                self.login()    
    
    #----------------------------------------------------------------------
    def login(self):
        """杩炴帴鏈嶅姟鍣�"""
        # 濡傛灉濉叆浜嗙敤鎴峰悕瀵嗙爜绛夛紝鍒欑櫥褰�
        if self.userID and self.password and self.brokerID:
            req = {}
            req['UserID'] = self.userID
            req['Password'] = self.password
            req['BrokerID'] = self.brokerID
            req['UserProductInfo'] = self.productInfo
            req['AuthCode'] = self.authCode             
            req['RandCode'] = self.randCode
            self.reqID += 1
            self.reqUserLogin(req, self.reqID)   
        
    #----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """鍙戝崟"""
        self.reqID += 1
        self.orderRef += 1
        
        req = {}
        
        req['InstrumentID'] = str(orderReq.symbol)
        req['LimitPrice'] = str(orderReq.price)     # LTS閲岀殑浠锋牸鏄瓧绗︿覆
        req['VolumeTotalOriginal'] = int(orderReq.volume)
        req['ExchangeID'] = exchangeMap.get(orderReq.exchange, '')
        
        # 涓嬮潰濡傛灉鐢变簬浼犲叆鐨勭被鍨嬫湰鎺ュ彛涓嶆敮鎸侊紝鍒欎細杩斿洖绌哄瓧绗︿覆
        try:
            req['OrderPriceType'] = priceTypeMap[orderReq.priceType]
            req['Direction'] = directionMap[orderReq.direction]
            req['CombOffsetFlag'] = offsetMap[orderReq.offset]
            req['ExchangeID'] = exchangeMap[orderReq.exchange]
        except KeyError:
            return ''
            
        req['OrderRef'] = str(self.orderRef)
        req['InvestorID'] = self.userID
        req['UserID'] = self.userID
        req['BrokerID'] = self.brokerID
        
        req['CombHedgeFlag'] = defineDict['SECURITY_FTDC_HF_Speculation']       # 鎶曟満鍗�
        req['ContingentCondition'] = defineDict['SECURITY_FTDC_CC_Immediately'] # 绔嬪嵆鍙戝崟
        req['ForceCloseReason'] = defineDict['SECURITY_FTDC_FCC_NotForceClose'] # 闈炲己骞�
        req['IsAutoSuspend'] = 0                                                # 闈炶嚜鍔ㄦ寕璧�
        req['TimeCondition'] = defineDict['SECURITY_FTDC_TC_GFD']               # 浠婃棩鏈夋晥
        req['VolumeCondition'] = defineDict['SECURITY_FTDC_VC_AV']              # 浠绘剰鎴愪氦閲�
        req['MinVolume'] = 1                                                    # 鏈�灏忔垚浜ら噺涓�1
        req['UserForceClose'] = 0
        
        self.reqOrderInsert(req, self.reqID)
        
        # 杩斿洖璁㈠崟鍙凤紙瀛楃涓诧級锛屼究浜庢煇浜涚畻娉曡繘琛屽姩鎬佺鐞�
        vtOrderID = '.'.join([self.gatewayName, str(self.orderRef)])
        return vtOrderID
    
    #----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """鎾ゅ崟"""
        self.reqID += 1

        req = {}
        
        req['InstrumentID'] = cancelOrderReq.symbol
        req['ExchangeID'] = cancelOrderReq.exchange
        req['OrderRef'] = cancelOrderReq.orderID
        req['FrontID'] = cancelOrderReq.frontID
        req['SessionID'] = cancelOrderReq.sessionID
        
        req['ActionFlag'] = defineDict['SECURITY_FTDC_AF_Delete']
        req['BrokerID'] = self.brokerID
        req['InvestorID'] = self.userID
        
        self.reqOrderAction(req, self.reqID)
        
    #----------------------------------------------------------------------
    def close(self):
        """鍏抽棴"""
        self.exit()
    
        
    