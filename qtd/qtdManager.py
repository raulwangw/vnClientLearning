from qtd.qtdListener import *
from qtd.qtdSerApiManager import *

class qtdManager(object):
    def __init__(self,mainEngine,eventEngine): 
        super(qtdManager,self).__init__()
        self.mainEngine = mainEngine
        self.eventEngine = eventEngine
        qtdListener.registed(1,self.eventEngine)
        self.apiManager = qtdSerApiManager()
                
    def queryStockInfor(self,dict):
        pass
    
    def customerStock(self,stockname):
        pass
    
    def queryPictureByStockName(self,stockName,picType):
        pass
    
    def queryLog(self):
        pass
    
    def testForKLine(self):
        self.apiManager.testForKLine()
        
    def testMD(self):
        self.apiManager.testMD()
        
    def getAllStockSelectionNames(self):
        return ["name1","name2"]
    
    def activeStockSelectionStratistic(self,sname):
        self.apiManager.activeStockSelectionStratistic(sname)