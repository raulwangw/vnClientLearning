from qtd.qtdBaseListener import *
from eventEngine import *

class qtdListener(qtdBaseListener):
    eventEngineDict={}
    def __init__(self):
        self(qtdListener,self).__init__()
    
    @staticmethod
    def registed(_id,obj):
        if not qtdListener.eventEngineDict.has_key(_id):
            qtdListener.eventEngineDict[_id] = obj

    @staticmethod
    def notify(_id,data):
        for evtid in qtdListener.eventEngineDict:
            eventEngine = qtdListener.eventEngineDict[evtid]
            event2 = Event(type_=_id)
            event2.dict_['data'] = data
            eventEngine.put(event2)
            

class __listenerNotify(object):
    def __init__(self):
        super(__listenerNotify,self).__init__()

        