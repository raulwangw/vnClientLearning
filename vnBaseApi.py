import os
import threading
import Queue
class vnBaseApi(object):
    def __init__(self):
        self.thd = None
    
    def createCusMdApi(self,path):
        err = ""
        if not os.path.isfile(path):
            err = "Path %s is not a existed file type file"%path
            #return False,err
        try:
            #self.st = open(path,'a+')
            pass
        except IOError,e:
            print e
            err = "can't open file %s"%path
            #return False,err
        
        return True,err
    
    def registerCmdCB(self,cmd,cb):
        if self.thd == None:
            self.thd = self.createApiThread()
            self.thd.start()

        self.thd.registerCmdCB(cmd,cb)
    
    def sendCommand(self,cmd,params={}):
        self.thd.setCommand(cmd,params)
    
    def createApiThread(self):
        # customer Api Thread
        print("td api !!!!!!!")
        return _privApiThread(self)
    
    def runCommand(self,cmd,param):
        #customer run command
        pass

    def exit(self):
        if self.thd != None:
            self.thd.stop()
        

class _privApiThread(threading.Thread):
    def __init__(self,api):
        super(_privApiThread,self).__init__()
        self.funcDict={}
        self.curRunCmd=None
        self.running = False
        self.hasCmd = False
        self.api = api
        self.queue = Queue.Queue(100)
    
    def registerCmdCB(self,cmd,cb):
        err=""
        if cmd in self.funcDict.keys():
            err = "Duplication Paramater"
            return False,err
        
        self.funcDict[cmd]=cb   
        return True,err
        
    def setCommand(self,cmd,params):
        if cmd in self.funcDict.keys() and self.running == True:
            self.queue.put({cmd:params})

    
    def run(self):
        self.running = True
        
        while self.running:
            dict = self.queue.get(True)
            if len(dict.keys()) == 0:
                continue
            print(dict)
            cmd = dict.keys()[0]
            param = dict[cmd]
            rst,rcmd = self.api.runCommand(cmd,param)
            if rst != None and rcmd != "" :
                self.funcDict[rcmd](rst)
            else :
                self.funcDict[rcmd]()
            dict.clear()
                
        self.running = False
    
    def runCommand(self,cmd):
        return False,""
    
    def stop(self):
        self.queue.put_nowait({})
        self.running = False
    
    
    
        
    
