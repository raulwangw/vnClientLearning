# encoding: UTF-8

'''
vn.Qtd的gateway接入
'''

import os
import json

from vnQtdmd import vnQtdMdApi
from vnQtdtd import vnQtdTdApi
from vnQtdqry import vnQtdQryApi
from qtdDataType import *
from vtGateway import *
from ctypes import *
import ctypes as ct

# 以下为一些VT类型和Qtd类型的映射字典
# 价格类型映射
priceTypeMap= {}

priceTypeMap[PRICETYPE_LIMITPRICE] = defineDict["SECURITY_FTDC_OPT_LimitPrice"]
priceTypeMap[PRICETYPE_MARKETPRICE] = defineDict["SECURITY_FTDC_OPT_AnyPrice"]
priceTypeMap[PRICETYPE_FAK] = defineDict["SECURITY_FTDC_OPT_BestPrice"]
priceTypeMap[PRICETYPE_FOK] = defineDict["SECURITY_FTDC_OPT_AllLimitPrice"]
priceTypeMapReverse = {v: k for k, v in priceTypeMap.items()} 

# 方向类型映射
directionMap = {}
directionMap[DIRECTION_LONG] = defineDict["SECURITY_FTDC_D_Buy"]
directionMap[DIRECTION_SHORT] = defineDict["SECURITY_FTDC_D_Sell"]
directionMapReverse = {v: k for k, v in directionMap.items()}

# 开平类型映射
offsetMap = {}
offsetMap[OFFSET_OPEN] = defineDict["SECURITY_FTDC_OF_Open"]
offsetMap[OFFSET_CLOSE] = defineDict["SECURITY_FTDC_OF_Close"]
offsetMap[OFFSET_CLOSETODAY] = defineDict["SECURITY_FTDC_OF_CloseToday"]
offsetMap[OFFSET_CLOSEYESTERDAY] = defineDict["SECURITY_FTDC_OF_CloseYesterday"]
offsetMapReverse = {v:k for k,v in offsetMap.items()}

# 交易所类型映射
exchangeMap = {}
exchangeMap[EXCHANGE_SSE] = 'SSE'
exchangeMap[EXCHANGE_SZSE] = 'SZE'
exchangeMap[EXCHANGE_HKEX] = 'HGE'
exchangeMapReverse = {v:k for k,v in exchangeMap.items()}

# 持仓类型映射
posiDirectionMap = {}
posiDirectionMap[DIRECTION_NET] = defineDict["SECURITY_FTDC_PD_Net"]
posiDirectionMap[DIRECTION_LONG] = defineDict["SECURITY_FTDC_PD_Long"]
posiDirectionMap[DIRECTION_SHORT] = defineDict["SECURITY_FTDC_PD_Short"]
posiDirectionMapReverse = {v:k for k,v in posiDirectionMap.items()}


########################################################################################
class QtdGateway(VtGateway):
    """Qtd接口"""

    #----------------------------------------------------------------------
    def __init__(self, eventEngine, gatewayName='QTD'):
        """Constructor"""
        print("__init__")
        super(QtdGateway, self).__init__(eventEngine, gatewayName)
        print("self")
        self.mdApi = QtdMdApi(self)
        self.tdApi = QtdTdApi(self)
        self.qryApi = QtdQryApi(self)
        
        self.mdConnected = False
        self.tdConnected = False
        self.qryConnected = False
        
        self.qryEnabled = False         # 是否要启动循环查询
        print("i__init__")
    
    #----------------------------------------------------------------------
    def connect(self):
        """连接"""
        print("qgw connect")
        # 载入json 文件
        fileName = self.gatewayName + '_connect.json'
        fileName = os.getcwd() + '/QtdGateway/' + fileName
        
        try:
            f = file(fileName)
        except IOError:
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'读取连接配置出错，请检查'
            self.onLog(log)
            return
        
        # 解析json文件
        setting = json.load(f)
        try:    
            userID = str(setting['userID'])
            mdPassword = str(setting['mdPassword'])
            tdPassword = str(setting['tdPassword'])
            brokerID = str(setting['brokerID'])            
            qryAddress = str(setting['qryAddress'])
            productInfo = str(setting['productInfo'])
            authCode = str(setting['authCode'])
            mdAddress = str(setting['mdAddress'])
            mdport = int(setting['mdport']) 
            tdAddress = str(setting['tdAddress'])
            tdport = str(setting['tdport'])
            tdver = str(setting['tdver'])
            YybID = str(setting['YybID'])
            AccountNo = str(setting['AccountNo'])
            TradeAccount = str(setting['TradeAccount'])
            JyPassword = str(setting['JyPassword'])
            TxPassword = str(setting['TxPassword']) 
            
        except KeyError:
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'连接配置缺少字段，请检查'
            self.onLog(log)
            return            
              
        # 创建行情和交易接口对象
        print("1")
        self.mdApi.connect(userID, mdPassword, brokerID, mdAddress, mdport)
        print(2)
        #self.tdApi.connect(tdAddress,tdport,tdver,YybID, AccountNo,TradeAccount,JyPassword,TxPassword)        
        
        # 初始化并启动查询
        #self.setQryEnabled(True)
        self.initQuery()
		
    #----------------------------------------------------------------------
    def subscribe(self, subscribeReq):
        """订阅行情"""
        print("qgw subscribe")
        self.mdApi.subscribe(subscribeReq)
        
    #----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """发单"""
        print("qgw sendOrder")
        return self.tdApi.sendOrder(orderReq)
        
    #----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """撤单"""
        print("qgw cancelOrder")
        self.tdApi.cancelOrder(cancelOrderReq)
        
    #----------------------------------------------------------------------
    def qryAccount(self):
        """查询账户资金"""
        print("qgw qryAccount")
        self.mdApi.qryAccount()
        
    #----------------------------------------------------------------------
    def qryPosition(self):
        """查询持仓"""
        pass
        #print("qgw qryPosition")
        #self.qryApi.qryPosition()
    
    def qryMarket(self):
        self.mdApi.qryMarket()
    
    
    #----------------------------------------------------------------------
    def close(self):
        """关闭"""
        if self.mdConnected:
            print("qgw close mdConnected")
            self.mdApi.close()
            
        if self.tdConnected:
            print("qgw close tdConnected")
            self.tdApi.close()
            
        if self.qryConnected:
            print("qgw close qryConnected")
            self.qryApi.close()
            
        
    #----------------------------------------------------------------------
    def initQuery(self):
        print("qgw initQuery")
        """初始化连续查询"""
        if self.qryEnabled:
            # 需要循环的查询函数列表
            self.qryFunctionList = [self.qryMarket]
            
            self.qryCount = 0           # 查询触发倒计时
            self.qryTrigger = 2         # 查询触发点
            self.qryNextFunction = 0    # 上次运行的查询函数索引            
            self.startQuery()
    
    #----------------------------------------------------------------------
    def query(self, event):
        """注册到事件处理引擎上的查询函数"""
        self.qryCount += 1
        
        if self.qryCount > self.qryTrigger:
            # 清空倒计时
            self.qryCount = 0
            
            # 执行查询函数
            function = self.qryFunctionList[self.qryNextFunction]
            function()
            
            # 计算下次查询函数的索引，如果超过了列表长度，则重新设为0
            self.qryNextFunction += 1
            if self.qryNextFunction == len(self.qryFunctionList):
                self.qryNextFunction = 0
    
    #----------------------------------------------------------------------
    def startQuery(self):
        print("qgw startQuery")
        """启动连续查询"""
        self.eventEngine.register(EVENT_TIMER, self.query)
    
    #----------------------------------------------------------------------
    def setQryEnabled(self, qryEnabled):
        print("qgw setQryEnabled")
        """设置是否要启动循环查询"""
        self.qryEnabled = qryEnabled    


########################################################################
class QtdMdApi(vnQtdMdApi):
    """Qtd行情API实现"""
    
    #----------------------------------------------------------------------
    def __init__(self, gateway):
        """Constructor"""
        print((vnQtdMdApi))
        print("QtdMdApi __init__")
        super(QtdMdApi, self).__init__()
        self.gateway = gateway                     #gateway对象
        self.gatewayName = gateway.gatewayName     #gateway对象名称
        self.reqID = EMPTY_INT                  # 操作请求编号
        
        self.connectionStatus = False           # 连接状态
        #self.loginStatus = False                # 登陆状态
        
        self.subscribedSymbols = set()
        
        self.userID = EMPTY_STRING          # 账号
        self.password = EMPTY_STRING        # 密码
        self.brokerID = EMPTY_STRING        # 经纪商代码
        self.address = EMPTY_STRING         # 服务器地址         
        self.port = EMPTY_STRING            # 服务器端口
    
    #----------------------------------------------------------------------
    def onFrontConnected(self,params):
        """服务器连接"""
        print("QtdMdApi onFrontConnected")
        self.connectionStatus = True
        
        self.gateway.mdConnected = True
        for subscribeReq in self.subscribedSymbols:
            self.subscribe(subscribeReq)
            
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = u'Qtd行情服务器连接成功'
        self.gateway.onLog(log)
        self.test()
    
    def test(self):
        #test TdxL2Hq_GetDetailTransactionData
        dict = {}
        dict["market"]=1
        dict["zqdm"]="600770"
        dict["start"]=0
        dict["count"]=5
        dict["zqdmA"]=["600770","600771","600772","600773","600774"]
        dict["marketA"]=[1,1,1,1,1]
        dict["Category"]=4
        dict["date"]= 20140101
        dict["filename"]="600700.TXT"
        dict["length"]=21971
        self.sendCommand("QuerySubData",dict)

        
    #----------------------------------------------------------------------
    def onFrontDisconnected(self,params):
        """服务器断开"""
        print("QtdMdApi onFrontDisconnected")
        needPs = 1
        if len(params) == needPs:
            n = params['n']
        else:
            self.logParamsError(needPs,len(params))
            return
        
        self.connectionStatus= False
        #self.loginStatus = False
        self.gateway.mdConnected = False
        
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = u'Qtd行情服务器连接断开'
        self.gateway.onLog(log) 
        
    #----------------------------------------------------------------------
    def onHeartBeatWarning(self, params):
        """心跳报警"""
        pass
    
    #----------------------------------------------------------------------
    def onRspError(self,params):
        """错误回报"""
        print("QtdMdApi onRspError")

        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = params.get('ErrorID',-1)
        err.errorMsg = params.get('ErrorMsg'.decode('gbk'),"No Error InforMation")
        err.additionalInfo = params.get("ErrorAddInfo".decode('gbk'),"")
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------         
    # no use
    def onRspUserLogin(self, params):
        print("login no use in Md")
        return
        """登陆回报"""
        print("QtdMdApi onRspUserLogin")
        # 如果登录成功，推送日志信息

        if error['ErrorID'] == 0:
            self.loginStatus = True
            self.gateway.mdConnected = True
            
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'行情服务器登录完成'
            self.gateway.onLog(log)
            
            # 重新订阅之前订阅的合约
            for subscribeReq in self.subscribedSymbols:
                self.subscribe(subscribeReq)
                
        # 否则，推送错误信息
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)    
    
    #----------------------------------------------------------------------      
    #no use  
    def onRspUserLogout(self, data, error, n, last):
        print("logout no use in Md")
        return
        """登出回报"""
        print("QtdMdApi onRspUserLogout")
        # 如果登出成功，推送日志信息
        needPs = 4
        if len(params) == needPs:
            data= params['data']
            err = params['err']
            n   = params['n']
            last= params['last']
        else:
            self.logParamsError(needPs,len(params))
            return

        if error['ErrorID'] == 0:
            self.loginStatus = False
            self.gateway.tdConnected = False
            
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'行情服务器登出完成'
            self.gateway.onLog(log)
                
        # 否则，推送错误信息
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)
            
    #----------------------------------------------------------------------  
    def onRspSubMarketData(self, params):
        """订阅合约回报"""
        # 通常不在乎订阅错误，选择忽略
        print("QtdMdApi onRspSubMarketData")
        needPs = 4
        if len(params) == needPs:
            data= params['data']
            err = params['err']
            n   = params['n']
            last= params['last']
        else:
            self.logParamsError(needPs,len(params))
            return
        
        
        #self.gateway.onContract()
        
    #----------------------------------------------------------------------  
    def onRspUnSubMarketData(self, params):
        """退订合约回报"""
        print("QtdMdApi onRspUnSubMarketData")
        # 同上
        needPs = 4
        if len(params) == needPs:
            data= params['data']
            err = params['err']
            n   = params['n']
            last= params['last']
        else:
            self.logParamsError(needPs,len(params))
            return
        print("onRsp subMarketData fail")
    
    #----------------------------------------------------------------------  
    def onRtnDepthMarketData(self, data):
        """行情推送"""
        print("QtdMdApi onRtnDepthMarketData")

        tick = VtTickData()
        tick.gatewayName = self.gatewayName
        
        
        
        tick.symbol = data['InstrumentID']
        tick.exchange = exchangeMapReverse.get(data['ExchangeID'], u'未知')
        tick.vtSymbol = '.'.join([tick.symbol, tick.exchange])
        print("vtSymbol"+tick.vtSymbol)
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
        
        # Qtd有5档行情
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
    def connect(self, userID, password, brokerID, address, port):
        """初始化连接"""
        print("QtdMdApi connect")
        self.userID = userID                # 账号
        self.password = password            # 密码
        self.brokerID = brokerID            # 经纪商代码
        self.address = address              # 服务器地址
        self.port = port;
        # 如果尚未建立服务器连接，则进行连接
        if not self.connectionStatus:
            # 创建C++环境中的API对象，这里传入的参数是需要用来保存.con文件的文件夹路径
            path = os.getcwd() + '/temp/' + self.gatewayName + '/'
            if not os.path.exists(path):
                os.makedirs(path)
            self.createCusMdApi(path)

            # 注册服务器地址
            self.registerFront(self.address,self.port)
        
            tick = {}
            tick["InstrumentID"]="iId"
            tick["ExchangeID"]="SSE"
            tick["LastPrice"]=3
            tick["Volume"]=4
            tick["OpenInterest"]=5
            tick["OpenInterest"]=6
            tick["UpdateTime"]="16:08:08"
            tick["UpdateMillisec"]=658
            tick["TradingDay"]=160809
            tick["OpenPrice"]=1.2
            tick["HighestPrice"]=1.3
            tick["LowestPrice"]=1.1
            tick["PreClosePrice"]=1.15
            tick["UpperLimitPrice"]=1.8
            tick["LowerLimitPrice"]=0.9
            tick["BidPrice1"]=1
            tick["BidVolume1"]=1.1
            tick["AskPrice1"]=2
            tick["AskVolume1"]=2.1
            
            tick["BidPrice2"]=1.02
            tick["BidVolume2"]=1.12
            tick["AskPrice2"]=2.02
            tick["AskVolume2"]=2.12
    
            tick["BidPrice3"]=1.03
            tick["BidVolume3"]=1.13
            tick["AskPrice3"]=2.03
            tick["AskVolume3"]=2.13
    
            tick["BidPrice4"]=1.04
            tick["BidVolume4"]=1.14
            tick["AskPrice4"]=2.04
            tick["AskVolume4"]=2.14
    
            tick["BidPrice5"]=1.05
            tick["BidVolume5"]=1.15
            tick["AskPrice5"]=2.05
            tick["AskVolume5"]=2.15

            self.onRtnDepthMarketData(tick)
            # 初始化连接，成功会调用onFrontConnected
            self.init()
        # 若已经连接但尚未登录，则进行登录
        #else:
            #if not self.loginStatus:
                #self.login()
    
    def qryMarket(self):
        pass
    
    #----------------------------------------------------------------------
    def subscribe(self, subscribeReq):
        """订阅合约"""
        print("QtdMdApi subscribe")
        req = {}
        req['InstrumentID'] = str(subscribeReq.symbol)
        req['ExchangeID'] = exchangeMap.get(str(subscribeReq.exchange), '')
        if self.connectionStatus:
            self.subscribeMarketData(req)
        else:
            if not subscribeReq in self.subscribedSymbols:
                self.subscribedSymbols.add(subscribeReq)
	
    #----------------------------------------------------------------------
    #no use
    def login(self):
        """登录"""
        return
        print("QtdMdApi login")
        # 如果填入了用户名密码等，则登录
        if self.userID and self.password and self.brokerID:
            req = {}
            req['UserID'] = self.userID
            req['Password'] = self.password
            req['BrokerID'] = self.brokerID
            self.reqID += 1
            self.reqUserLogin(req, self.reqID)    

    #----------------------------------------------------------------------
    def close(self):
        """关闭"""
        print("QtdMdApi close")
        self.exit()
	        
########################################################################
class QtdTdApi(vnQtdTdApi):
    """Qtd交易API实现"""
    #----------------------------------------------------------------------
    def __init__(self, gateway):
        """API对象的初始化函数"""
        super(QtdTdApi, self).__init__()
        
        self.gateway = gateway                  # gateway对象
        self.gatewayName = gateway.gatewayName  # gateway对象名称
        
        self.reqID = EMPTY_INT              # 操作请求编号
        self.orderRef = EMPTY_INT           # 订单编号
        
        self.connectionStatus = False       # 连接状态
        self.loginStatus = False            # 登录状态
        
        self.tdAddress = EMPTY_STRING    #address
        self.tdport = EMPTY_STRING       #port
        self.tdver = EMPTY_STRING        #trder version
        self.YybID = EMPTY_STRING        #Yyb id
        self.AccountNo = EMPTY_STRING    #count number
        self.TradeAccount = EMPTY_STRING #trader count
        self.JyPassword = EMPTY_STRING   #JY的password
        self.TxPassword = EMPTY_STRING   #TX的password
        #tdAddress,tdport,tdver,YybID, AccountNo,TradeAccount,JyPassword,TxPassword
    #----------------------------------------------------------------------
    def onFrontConnected(self,params):
        """服务器连接"""
        self.connectionStatus = True
        
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = u'交易服务器连接成功'
        self.gateway.onLog(log)
        
        # 前置机连接后，请求随机码
        self.reqID += 1
        #self.reqFetchAuthRandCode({}, self.reqID)
        self.sendCommand("UserLogOn")        
    
    #----------------------------------------------------------------------
    def onFrontDisconnected(self, n):
        """服务器断开"""
        self.connectionStatus = False
        self.loginStatus = False
        self.gateway.tdConnected = False
        
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = u'交易服务器连接断开'
        self.gateway.onLog(log)      
    
    #----------------------------------------------------------------------
    def onHeartBeatWarning(self, n):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def onRspUserLogin(self, params):
        """登陆回报"""
        return
        # 如果登录成功，推送日志信息
        if error['ErrorID'] == 0:
            self.loginStatus = True
            self.gateway.mdConnected = True
            
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'交易服务器登录完成'
            self.gateway.onLog(log)            
                
        # 否则，推送错误信息
        else:
            err = VtErrorData()
            err.gatewayName = self.gateway
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspUserLogout(self, data, error, n, last):
        """登出回报"""
        # 如果登出成功，推送日志信息
        if error['ErrorID'] == 0:
            self.loginStatus = False
            self.gateway.tdConnected = False
            
            log = VtLogData()
            log.gatewayName = self.gatewayName
            log.logContent = u'交易服务器登出完成'
            self.gateway.onLog(log)
                
        # 否则，推送错误信息
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspFetchAuthRandCode(self, data, error, n, last):
        """请求随机认证码"""
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
        """发单错误（柜台）"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspOrderAction(self, data, error, n, last):
        """撤单错误（柜台）"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspError(self, params):
        """错误回报"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = params.get('ErrorID',-1)
        err.errorMsg = params.get('ErrorMsg'.decode('gbk'),"No Error InforMation")
        err.additionalInfo = params.get("ErrorAddInfo".decode('gbk'),"")
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRtnOrder(self, data):
        """报单回报"""       
        # 更新最大报单编号
        newref = data['OrderRef']
        self.orderRef = max(self.orderRef, int(newref))
        
        # 创建报单数据对象
        order = VtOrderData()
        order.gatewayName = self.gatewayName
        
        # 保存代码和报单号
        order.symbol = data['InstrumentID']
        order.exchange = exchangeMapReverse.get(data['ExchangeID'], '')
        order.vtSymbol = '.'.join([order.symbol, order.exchange])
        
        order.orderID = data['OrderRef']
        
        # 方向
        if data['Direction'] == '0':
            order.direction = DIRECTION_LONG
        elif data['Direction'] == '1':
            order.direction = DIRECTION_SHORT
        else:
            order.direction = DIRECTION_UNKNOWN
            
        # 开平
        if data['CombOffsetFlag'] == '0':
            order.offset = OFFSET_OPEN
        elif data['CombOffsetFlag'] == '1':
            order.offset = OFFSET_CLOSE
        else:
            order.offset = OFFSET_UNKNOWN
            
        # 状态
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
            
        # 价格、报单量等数值
        order.price = float(data['LimitPrice'])
        order.totalVolume = data['VolumeTotalOriginal']
        order.tradedVolume = data['VolumeTraded']
        order.orderTime = data['InsertTime']
        order.cancelTime = data['CancelTime']
        order.frontID = data['FrontID']
        order.sessionID = data['SessionID']
        
        # CTP的报单号一致性维护需要基于frontID, sessionID, orderID三个字段
        order.vtOrderID = '.'.join([self.gatewayName, order.orderID])
        
        # 推送
        self.gateway.onOrder(order)
    
    #----------------------------------------------------------------------
    def onRtnTrade(self, data):
        """成交回报"""
        # 创建报单数据对象
        trade = VtTradeData()
        trade.gatewayName = self.gatewayName
        
        # 保存代码和报单号
        trade.symbol = data['InstrumentID']
        trade.exchange = exchangeMapReverse.get(data['ExchangeID'], '')
        trade.vtSymbol = '.'.join([trade.symbol, trade.exchange])
        
        trade.tradeID = data['TradeID']
        trade.vtTradeID = '.'.join([self.gatewayName, trade.tradeID])
        
        trade.orderID = data['OrderRef']
        trade.vtOrderID = '.'.join([self.gatewayName, trade.orderID])   
        
        # 方向
        trade.direction = directionMapReverse.get(data['Direction'], '')
            
        # 开平
        trade.offset = offsetMapReverse.get(data['OffsetFlag'], '')
            
        # 价格、报单量等数值
        trade.price = float(data['Price'])
        trade.volume = data['Volume']
        trade.tradeTime = data['TradeTime']
        
        # 推送
        self.gateway.onTrade(trade)
    
    #----------------------------------------------------------------------
    def onErrRtnOrderInsert(self, data, error):
        """发单错误回报（交易所）"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onErrRtnOrderAction(self, data, error):
        """撤单错误回报（交易所）"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)
    
    #----------------------------------------------------------------------
    def onRspFundOutByLiber(self, data, error, n, last):
        """Qtd发起出金应答"""
        pass   
 
    #----------------------------------------------------------------------    
    def onRtnFundOutByLiber(self, data):
        """Qtd发起出金通知"""
        pass        
    
    #----------------------------------------------------------------------
    def onErrRtnFundOutByLiber(self, data, error):
        """Qtd发起出金错误回报"""
        pass
    
    #----------------------------------------------------------------------
    def onRtnFundInByBank(self, data):
        """银行发起入金通知"""
        pass

    #----------------------------------------------------------------------
    def onRspFundInterTransfer(self, data, error, n, last):
        """资金内转应答"""
        pass
    
    #----------------------------------------------------------------------
    def onRtnFundInterTransferSerial(self, data):
        """资金内转流水通知"""
        pass
    
    #----------------------------------------------------------------------
    def onErrRtnFundInterTransfer(self, data, error):
        """资金内转错误回报"""
        pass  
         
    #----------------------------------------------------------------------
    #def connect(self, userID, password, brokerID, address, productInfo, authCode):
    def connect(self,tdAddress,tdport,tdver,YybID, AccountNo,TradeAccount,JyPassword,TxPassword):
        """初始化连接"""
        self.tdAddress = tdAddress                # 账号
        self.tdport = tdport            # 密码
        self.tdver = tdver            # 经纪商代码
        self.YybID = YybID              # 服务器地址
        self.AccountNo = AccountNo
        self.TradeAccount = TradeAccount
        self.JyPassword = JyPassword
        self.TxPassword = TxPassword
        # 如果尚未建立服务器连接，则进行连接
        if not self.connectionStatus:
            # 创建C++环境中的API对象，这里传入的参数是需要用来保存.con文件的文件夹路径
            path = os.getcwd() + '/temp/' + self.gatewayName + '/'
            if not os.path.exists(path):
                os.makedirs(path)
            self.createCusTraderApi(path)

            # 设置数据同步模式为推送从今日开始所有数据
            #self.subscribePrivateTopic(0)
            #self.subscribePublicTopic(0)

            # 注册服务器地址
            self.registerFront(self.tdAddress,self.tdport)

            # 初始化连接，成功会调用onFrontConnected
            self.init()

        # 若已经连接但尚未登录，则进行登录
        else:
            if not self.loginStatus:
                self.login()    
    
    #----------------------------------------------------------------------
    def login(self):
        """连接服务器"""
        # 如果填入了用户名密码等，则登录
        if self.YybID and self.tdver and self.AccountNo and self.TradeAccount:
            req = {}
            req['YybID'] = self.YybID
            req['Tdver'] = self.tdver
            req['AccountNo'] = self.AccountNo
            req['TradeAccount'] = self.TradeAccount
            req['JyPassword'] = self.JyPassword
            req['TxPassword'] = self.TxPassword
            self.reqID += 1
            self.reqUserLogin(req, self.reqID)   
        
    #----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """发单"""
        self.reqID += 1
        self.orderRef += 1
        
        req = {}
        
        req['InstrumentID'] = str(orderReq.symbol)
        req['LimitPrice'] = str(orderReq.price)     # Qtd里的价格是字符串
        req['VolumeTotalOriginal'] = int(orderReq.volume)
        req['ExchangeID'] = exchangeMap.get(orderReq.exchange, '')
        
        # 下面如果由于传入的类型本接口不支持，则会返回空字符串
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
        
        req['CombHedgeFlag'] = defineDict['SECURITY_FTDC_HF_Speculation']       # 投机单
        req['ContingentCondition'] = defineDict['SECURITY_FTDC_CC_Immediately'] # 立即发单
        req['ForceCloseReason'] = defineDict['SECURITY_FTDC_FCC_NotForceClose'] # 非强平
        req['IsAutoSuspend'] = 0                                                # 非自动挂起
        req['TimeCondition'] = defineDict['SECURITY_FTDC_TC_GFD']               # 今日有效
        req['VolumeCondition'] = defineDict['SECURITY_FTDC_VC_AV']              # 任意成交量
        req['MinVolume'] = 1                                                    # 最小成交量为1
        req['UserForceClose'] = 0
        
        self.reqOrderInsert(req, self.reqID)
        
        # 返回订单号（字符串），便于某些算法进行动态管理
        vtOrderID = '.'.join([self.gatewayName, str(self.orderRef)])
        return vtOrderID
    
    #----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """撤单"""
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
        """关闭"""
        self.exit()
        
class QtdQryApi(vnQtdQryApi):
    def __init__(self,gateway):
        super(QtdQryApi,self).__init__()

