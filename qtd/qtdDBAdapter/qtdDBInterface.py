#coding:UTF-8
from pymongo import MongoClient


class qtdDBInterface(object):
    def __init__(self):
        pass
    
    def initDb(self):
        client = MongoClient()

    

class qtdDBScanner(object):
    def __init__(self,scanFilepath):
        pass
    
    def _scanStockSelectStratistic(self):
        pass
    
    def _scanStockStratistic(self):
        pass
    
    def _scanRiskMonitorStratistic(self):
        pass
    
    def _scanDBDataIntegrity(self):
        pass