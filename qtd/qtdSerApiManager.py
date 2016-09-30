from qtd.qtdSerApi import *
class qtdSerApiManager(object):
    def __init__(self):
        self.api = qtdSerApi()
        
    
    def testMD(self):
        self.api.testMD()
    
    def testForKLine(self):
        self.api.testForKLine()
        
    def activeStockSelectionStratistic(self,sname):
        self.api.activeStockSelectionStratistic(sname)
        
    